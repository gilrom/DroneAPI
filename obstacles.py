import matplotlib.pyplot as plt
from shapely.geometry import Polygon,Point,box,LineString
import pandas as pd

obs = pd.read_csv("obstacles_100m_above_sea_level.csv")
types = obs["obs type"].unique()
polygons = []
for type in types:
    df = obs[obs["obs type"] == type]
    print(df)
    coords = []
    for index, row in df.iterrows():
        print(row)
        coord = (row["x obs meter"], row["y obs meter"])
        coords.append(coord)
        # print(coord)
    polygons.append(Polygon(coords))

fig = plt.figure()
plot = plt.subplot(1,1,1)
for pol in polygons:
    x,y = pol.exterior.xy
    plot.plot(x,y)
plot.invert_xaxis()
plt.show()