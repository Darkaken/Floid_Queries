
import pickle

from accounts import importData, Account, AccountContainer
from statistics import stdev, mean
import statistics

import matplotlib.pyplot as plt
import numpy as np

def getStats(report):

    returnDict = {
        "general_data": {},
        "stdev": {}
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

    try:
        returnDict["general_data"]["ratio"] = returnDict["general_data"]["total_in"] / returnDict["general_data"]["total_out"]
    except:
        returnDict["general_data"]["ratio"] = "Undefined"

    inflow = [x for x in report.transactions if x[2] != 0]
    outflow = [x for x in report.transactions if x[3] != 0]

    timeDict = {
        "inflow": {},
        "outflow": {},
        "total": {}
    }

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

    returnDict["general_data"]["avg_in"] = round(mean([x[2] for x in inflow]), 2)
    returnDict["general_data"]["avg_out"] = round(mean([x[3] for x in outflow]), 2)

    try:
        returnDict["stdev"]["Stdev_In"] = round(stdev(timeDict["inflow"].values()), 2)
    except statistics.StatisticsError:
        returnDict["stdev"]["Stdev_In"] = 0

    try:
        returnDict["stdev"]["Stdev_Out"] = round(stdev(timeDict["outflow"].values()), 2)
    except statistics.StatisticsError:
        returnDict["stdev"]["Stdev_Out"] = 0

    try:
        returnDict["stdev"]["Stdev_Net"] = round(stdev(timeDict["total"].values()), 2)
    except statistics.StatisticsError:
        returnDict["stdev"]["Stdev_Net"] = 0

    if True:
    #if False:

        createBar(timeDict["outflow"].keys(), timeDict["outflow"].values(), "Outflow")
        createBar(timeDict["inflow"].keys(), timeDict["inflow"].values(), "Inflow")
        createBar(timeDict["total"].keys(), timeDict["total"].values(), "Total")

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

def filterContainer(container):

    newCont = []

    for item in container.accounts:
        if len(item.transactions) > 30:
            newCont.append(item)

    return newCont

container = importData(all_banks=True)

print(getStats(container.accounts[15]))


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