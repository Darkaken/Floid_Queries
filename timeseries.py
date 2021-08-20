
import pickle
import matplotlib.pyplot as plt
from datetime import date, datetime, timedelta

class BalanceHistory(object):
    globalcounternotassets = 0
    globalcounterNoneType = 0
    globalinfo = 0

    def __init__(self, reportId, transactions, balance):

        self.reportId = reportId
        self.balance = balance
        self.balance_list = self.completebalancelist(self.construct(transactions))
        self.maketimeseries(step = 30, save=True)

        self.balance_list = self.construct(transactions)
        self.maketimeseries(step = 3, save=True, filenameModifier = "_simplified")

    @staticmethod
    def completebalancelist(balance_list):

        last_date = [int(x) for x in balance_list[0][0].split("-")]
        start_date = [int(x) for x in balance_list[-1][0].split("-")]

        sdate = date(start_date[0], start_date[1], start_date[2])
        edate = date(last_date[0], last_date[1], last_date[2])

        delta = edate - sdate  # as timedelta

        date_list = [(sdate + timedelta(days = x)).strftime('%Y-%m-%d') for x in range(delta.days + 1)][::-1]
        balances = []

        balance_list = balance_list

        current_balance = balance_list[0][1]
        for datePoint in date_list:

            for balanceItem in balance_list:

                if datePoint == balanceItem[0]:
                    current_balance = balanceItem[1]

            balances.append(current_balance)

        return [[date_list[i], balances[i]] for i in range(len(date_list))]

    def construct(self, transactions):

        #for transaction in transactions:
        #    print(transaction)

        timelist = self.createtimelist(transactions)
        change_list = [0 for x in range(len(timelist))]

        for i in range(len(timelist)):
            for transaction in transactions:
                if transaction["date"] == timelist[i]:
                    change_list[i] += transaction["out"]
                    change_list[i] -= transaction["in"]

        balance_list = [self.balance]

        current = self.balance
        for item in change_list:
            current += item
            balance_list.append(current)

        if min(balance_list) < 0:
            return -1

        recent_date = [int(x) for x in timelist[0].split("-")]
        recent_date = date(recent_date[0], recent_date[1], recent_date[2])

        timelist.insert(0, (recent_date + timedelta(days = 1)).strftime('%Y-%m-%d'))

        return [[timelist[x], balance_list[x]] for x in range(len(timelist))]

    def maketimeseries(self, step, save = False, filenameModifier = ""):

        balance_list = self.balance_list[::-1]

        x = [item[0] for item in balance_list]
        y = [item[1] for item in balance_list]

        x_0 = []
        count = 0
        for item in x:

            if count == 0:
                x_0.append(item)
                count += 1
            elif count == step:
                x_0.append(" ")
                count = 0
            else:
                x_0.append(" ")
                count += 1

        plt.figure(dpi = 1200)

        plt.plot(x, y, "-ok", markersize=2)
        plt.xticks(x, labels=x_0, rotation=45, fontsize = 8)
        plt.xlabel("Date", fontsize = 15)
        plt.ylabel("Balance", fontsize = 15)

        plt.title(f"Serie de Tiempo de {self.reportId}")
        plt.tight_layout()

        if save:
            plt.savefig(f"TimeSeries/{self.reportId}{filenameModifier}")

        plt.show()

    @staticmethod
    def createtimelist(transactions):

        timelist = []
        for transaction in transactions:
            if transaction["date"] not in timelist:
                timelist.append(transaction["date"])

        return timelist


def timeseriesbyid(reportId):

    try:

        selected = None
        for item in container:
            if item["reportId"] == reportId:
                selected = item

        if selected is None:
            return -1

        try:
            len(selected["assets"]["accounts"])
        except KeyError:
            BalanceHistory.globalcounternotassets += 1
            return -1

        balance = 0
        for account in selected["assets"]["accounts"]:
            try:
                if account["balance"] > balance:
                    balance = account["balance"]
            except KeyError:   #Si una cuenta no tiene un balance
                pass

        #print(f"Balance: {balance}")

        balancehistory = BalanceHistory(reportId, selected["transactions"], balance)

    except Exception as e:
        BalanceHistory.globalcounterNoneType += 1


with open("Data/all_data.pickle", "rb") as infile:
    container = pickle.load(infile)

timeseriesbyid("c910ad1e-3d9a-407c-aee2-0f5893a02d00")

def test():
    for item in container:
        result = timeseriesbyid(item["reportId"])

        if result is None:
            print(item["reportId"])

#timeseriesbyid(container[25]["reportId"])


