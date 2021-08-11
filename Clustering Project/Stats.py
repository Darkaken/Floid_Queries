
import pickle

from accounts import duplicateFiltering, accountGen
from statistics import stdev, mean
import statistics

from sklearn import preprocessing

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

bankname = "santander"

def getStats(report):

    returnDict = {
        "general_data": {},
    }

    try:
        returnDict["general_data"]["total_in"] = sum([x[2] for x in report.transactions])
    except:
        returnDict["general_data"]["total_in"] = 0

    try:
        returnDict["general_data"]["total_out"] = sum([x[3] for x in report.transactions])
    except:
        returnDict["general_data"]["total_out"] = 0

    returnDict["general_data"]["diferencia_neta"] = returnDict["general_data"]["total_in"] - returnDict["general_data"]["total_out"]

    inflow = [x for x in report.transactions if x[2] != 0]
    outflow = [x for x in report.transactions if x[3] != 0]

    timeDict = {
        "inflow": {},
        "outflow": {},
        "total": {}
    }

    try:

        for item in inflow:

            try:
                timeDict["inflow"][item[0]] += item[2]
                timeDict["total"][item[0]] += item[2]
            except:
                timeDict["inflow"][item[0]] = item[2]
                timeDict["total"][item[0]] = item[2]

        for item in outflow:

            try:
                timeDict["outflow"][item[0]] += item[3]
                timeDict["total"][item[0]] -= item[3]
            except:
                timeDict["outflow"][item[0]] = item[3]

                try:
                    timeDict["total"][item[0]] -= item[3]
                except:
                    timeDict["total"][item[0]] = -item[3]

        returnDict["general_data"]["in_transactions"] = len(inflow)
        returnDict["general_data"]["out_transactions"] = len(outflow)

        try:
            returnDict["general_data"]["Stdev_In"] = round(stdev(timeDict["inflow"].values()), 2)
        except statistics.StatisticsError:
            returnDict["general_data"]["Stdev_In"] = 0

        try:
            returnDict["general_data"]["Stdev_Out"] = round(stdev(timeDict["outflow"].values()), 2)
        except statistics.StatisticsError:
            returnDict["general_data"]["Stdev_Out"] = 0

        try:
            returnDict["general_data"]["Stdev_Net"] = round(stdev(timeDict["total"].values()), 2)
        except statistics.StatisticsError:
            returnDict["general_data"]["Stdev_Net"] = 0

        returnDict["general_data"]["avg_in"] = round(mean([x for x in timeDict["inflow"].values()]), 2)
        returnDict["general_data"]["avg_out"] = round(mean([x for x in timeDict["outflow"].values()]), 2)

        #if True:
        if False:

            createBar(timeDict["outflow"].keys(), timeDict["outflow"].values(), "Outflow")
            createBar(timeDict["inflow"].keys(), timeDict["inflow"].values(), "Inflow")
            createBar(timeDict["total"].keys(), timeDict["total"].values(), "Total")

    except:
        return -1

    return returnDict

def createBar(time_list, number_list, title):

    ypos = np.arange(len(time_list))
    plt.xticks(ypos, time_list)
    plt.title(title)
    plt.xlabel("Fecha")
    if title != "Total":
        plt.ylabel("Cantidad (millones)")
    else:
        plt.ylabel("Cantidad")
    plt.bar(ypos, number_list, label="Montos")
    plt.show()

def createMatrix(container):

    matrix = []
    all_returns = [[getStats(item), item.reportId] for item in container.accounts if getStats(item) != -1]

    for item in all_returns:

        matrix.append([x for x in item[0]["general_data"].values()])

    matrix = np.array(matrix)

    dataFrame = pd.DataFrame(data = matrix, columns = ["total_in", "total_out", "total_diff", "in_transactions", "out_transactions", "avg_in", "avg_out", "stdev_in", "stdev_out", "stdv_diff"])

    dataFrame = pd.DataFrame(preprocessing.MinMaxScaler().fit_transform(dataFrame), columns = dataFrame.columns, index = dataFrame.index)

    ids = []
    for item in all_returns:
        ids.append(item[1])

    dataFrame["id"] = ids

    return dataFrame

def createCsv(dataFrame):

    dataFrame.to_csv(f"matrix_{bankname}.csv", encoding = "utf-8", index = False, sep = ",", header = False)

with open("../Data/all_data.pickle", "rb") as infile:
    container = pickle.load(infile)

data = [[x["reportId"], x["transactions"]] for x in container if type(x) == dict and x["bank"] == bankname]

container2 = accountGen(duplicateFiltering(data))

createCsv(createMatrix(container2))

"""
Restriction para arbol

Suma(ingresos + gastos) > X (x = ammount)
min_transaction_ammount > 10.000


"""

"""
Distancia vectorial

1) Vectorizar reporte
2) Definir Metrica

Dendograma
Propuesta del vector de features que vamos a usar (returnDict)

"""