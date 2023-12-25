import matplotlib.pyplot as plt
import rasterio.plot
import geopandas as gpd
from sqlalchemy import create_engine
from datetime import date, timedelta

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = date(2022, 2, 24)
end_date = date(2023, 12, 19)
i = 0

db_connection_url = "postgresql://postgres:****************@localhost:5432/postgres"
con = create_engine(db_connection_url)

for single_date in daterange(start_date, end_date):
    i = i + 1
    now_date = single_date.strftime("%d.%m.%Y")
    print(now_date)
    raster = rasterio.open("back2.tiff")
    fig, ax = plt.subplots(figsize=(16, 9))
    rasterio.plot.show(raster, ax=ax)
    plt.xlim([2299806.881, 4770718.883])
    plt.ylim([5504132.188, 6894020.189])
    plt.axis('off')
    ax.text(4350000, 6800000, now_date, fontsize=20, color='black')
    sql = '''select date,
        0.1 + 0.9/(1 + 0.1 * (TO_DATE(\'''' + now_date + '''\', 'DD.MM.YYYY') - date)) as alpha, 
        geom
        from events_all
        where date <= TO_DATE(\'''' + now_date + '''\', 'DD.MM.YYYY');'''
    df = gpd.GeoDataFrame.from_postgis(sql, con)
    df.plot(ax=ax, markersize=7, color='red', edgecolor='none', alpha = df['alpha'])
    plt.savefig('out/events_' + str(i).zfill(3) + '.png', bbox_inches='tight', pad_inches=0, dpi=207.8)
    plt.cla()
    plt.close()