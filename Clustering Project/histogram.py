import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

labels = ["0-300k", "300k-600k", "600k-900k", "900k-1.2M", "1.2M-1.5M", "1.5M-1.8M", "1.8M-2.1M", "2.1M-2.4M", "2.4M-2.7M", "2.7M-3M", "3M-10M", "-10M+"]

def histogram():

    incomefreq, expensefreq = getdata()

    plt.hist(incomefreq, label = "Income")
    plt.hist(expensefreq, label = "Expense")

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, incomefreq, width, label='Income')
    rects2 = ax.bar(x + width / 2, expensefreq, width, label='Expense')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Cantidad de Reportes')
    ax.set_title('Cantidad de reportes por tramo de ingreso/gasto')
    ax.set_xticks(x)
    ax.set_xticklabels([x.split("-")[1] for x in labels])
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()

    plt.show()

def getdata():

    data = pd.read_csv("matrix_not_normalized.csv")

    income_frecuency = getfreq(data.iloc[:, 5], [0 for x in range(len(labels))])
    expense_frecuency = getfreq(data.iloc[:, 6], [0 for x in range(len(labels))])

    return income_frecuency, expense_frecuency

def getfreq(data, freq_list):

    for i in data:
        if 1 <= i <= 300000:
            freq_list[0] += 1
        elif 300000 < i <= 600000:
            freq_list[1] += 1
        elif 600000 < i <= 900000:
            freq_list[2] += 1
        elif 900000 < i <= 1200000:
            freq_list[3] += 1
        elif 1200000 < i <= 1500000:
            freq_list[4] += 1
        elif 1500000 < i <= 1800000:
            freq_list[5] += 1
        elif 1800000 < i <= 2100000:
            freq_list[6] += 1
        elif 2100000 < i <= 2400000:
            freq_list[7] += 1
        elif 2400000 < i <= 2700000:
            freq_list[8] += 1
        elif 2700000 < i <= 3000000:
            freq_list[9] += 1
        elif 3000000 < i <= 10000000:
            freq_list[9] += 1
        elif 10000000 < i:
            freq_list[10] += 1

    print(freq_list)
    return freq_list


histogram()