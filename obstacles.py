import matplotlib.pyplot as plt
from shapely.geometry import Polygon,Point,box,LineString
import pandas as pd
import numpy as np

obs = pd.read_csv("obstacles_100m_above_sea_level.csv")
types = obs["obs type"].unique()
polygons = []
for type in types:
    df = obs[obs["obs type"] == type]
    print(df)
    coords = []
    for index, row in df.iterrows():
        coord = (row["x obs meter"], row["y obs meter"])
        coords.append(coord)
    x_coords = [x for (x,y)in coords]
    y_coords = [y for (x,y)in coords]
    polygons.append(box(np.min(x_coords), np.min(y_coords), np.max(x_coords), np.max(y_coords)))

fig = plt.figure()
plot = plt.subplot(1,1,1)
for pol in polygons:
    x,y = pol.exterior.xy
    plot.plot(x,y)
plot.invert_xaxis()
plt.show()