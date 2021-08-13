import pickle
from sklearn.cluster import MeanShift
import numpy as np
import pandas as pd
import plotly.figure_factory as ff

bankname = "santander"
conversion_list = ["total_in", "total_out", "total_diff", "in_transactions", "out_transactions", "avg_in", "avg_out", "stdev_in", "stdev_out", "stdv_diff"]
request_id = ["0fde7722-34cb-484b-8bd6-76668361c65f", "5a33970e-1701-418b-8267-179929cd2b08", "b111bf65-ab0e-494f-9c96-ad30986b6f52", "c9e83931-34d6-4db7-9d96-c1305bd0bcb4"]

def regular_clustering():

    predictor = pd.read_csv(f"matrix_{bankname}.csv")
    trainer = predictor.iloc[: , :-1]

    print(trainer)

    ms = MeanShift()
    ms.fit(trainer)
    labels = ms.labels_

    cluster_centers = ms.cluster_centers_

    n_clusters_ = len(np.unique(labels))

    print("Number of Clusters: ", n_clusters_)
    #print("Cluster Centers:")

    #for center in cluster_centers:
    #    print(center)

    data = trainer.to_numpy()

    names = predictor.iloc[: , -1].tolist()

    names2 = []
    for name in names:
        if name not in request_id:
            names2.append("")
        else:
            names2.append(name)
            print("True")

    fig = ff.create_dendrogram(data, labels = names2)
    fig.update_layout(width = 800, height = 500)
    fig.write_html("fig_santander.html")

def column_clustering(column_index):

    predictor = pd.read_csv(f"matrix_{bankname}.csv")
    trainer = predictor.iloc[:, column_index]

    #print(trainer)

    data_a = trainer.to_numpy()
    data_zero = np.array(([0 for x in range(len(trainer))]))
    data = np.c_[data_a, data_zero]

    names = predictor.iloc[:, -1].tolist()

    names2 = []
    for name in names:
        if name not in request_id:
            names2.append("")
        else:
            names2.append(name)
            #print("True")

    #print(data.shape)

    fig = ff.create_dendrogram(data, labels=names2)
    fig.update_layout(width=800, height=500)
    fig.write_html(f"Santander_Figs/fig_santander_{conversion_list[column_index]}.html")

for i in range(10):
    column_clustering(i)