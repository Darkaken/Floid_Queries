import pickle
import numpy
from sklearn.cluster import MeanShift
import numpy as np
import pandas as pd
import plotly.figure_factory as ff

predictor = pd.read_csv("matrix.csv")

ms = MeanShift()
ms.fit(predictor)
labels = ms.labels_

cluster_centers = ms.cluster_centers_

n_clusters_ = len(np.unique(labels))

print("Number of Clusters: ", n_clusters_)
print("Cluster Centers:")

for center in cluster_centers:
    print(center)

fig = ff.create_dendrogram(predictor.to_numpy())
fig.update_layout(width = 800, height = 500)
fig.write_html("fig.html")

#colors = 10 * ["r.", "g.", "b.", "c.", "k.", "y.", "m."]

#for i in range(len(predictor)):
#    plt.plot(predictor[i][0], predictor[i][1], colors[labels[i]], markersize = 10)

#plt.scatter(cluster_centers[:, 0], cluster_centers[:, 1], marker = "x", s = 150, linewidths = 5, zorder = 10)

#plt.show()