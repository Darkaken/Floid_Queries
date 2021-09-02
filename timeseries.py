
import pickle
import matplotlib.pyplot as plt
from datetime import date, datetime, timedelta
from fake_report import fake_report
from decimal import Decimal
from statistics import mean

class BalanceHistory(object):

    globalcounternotassets = 0
    globalcounterNoneType = 0
    globalinfo = 0

    def __init__(self, reportId, transactions, balance):

        self.reportId = reportId
        self.balance = balance
        self.balance_list = self.completebalancelist(self.construct(transactions))
        #self.maketimeseries(step = 30, save=False)

        self.balance_list = self.construct(transactions)
        self.getMonthlyBurnRate()
        #self.maketimeseries(step = 3, save=False, filenameModifier = "_simplified")

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

    def getMonthlyBurnRate(self):

        monthly_dict = {}

        for balance in self.balance_list:

            if balance[0][:-3] not in monthly_dict.keys():
                monthly_dict[balance[0][:-3]] = [balance[1]]
            else:
                monthly_dict[balance[0][:-3]].append(balance[1])

        monthly_dict_max = {}

        for key, values in reversed(monthly_dict.items()):
            monthly_dict_max[key] = max(values)

        #print(monthly_dict_max)

        burnTimes = []
        time_matrix = []
        for value in monthly_dict_max.values():
            #burnTimes.append(self.burnTime(value, 1))
            time_matrix.append(self.burnToMaxPercentage(value))

        #print(burnTimes)
        #print(time_matrix)

    def burnToMaxPercentage(self, balance_value, percentages = (10, 20, 30, 40, 50, 60, 70, 80, 90, 100)):

        balance_date = None
        next_balances = None

        for item in self.balance_list:
            if item[1] == balance_value:
                balance_date = item[0]
                next_balances = [x for x in reversed(self.balance_list[:self.balance_list.index(item)])]
                break

        if balance_date is None or next_balances is None:
            raise Exception("Error de balance date o transaccion previa (self.burnRate())")

        if next_balances == []:
            return -1

        #print(balance_value)
        #print(balance_date)
        #print("###########")

        timelist = []
        for percentage in percentages:
            multiplier = (100 - percentage) / 100
            #print(float(balance_value) * float(multiplier))
            for balance in next_balances:
                if balance[1] <= float(balance_value) * float(multiplier):
                    timelist.append([percentage, balance[0]])
                    break

        print(timelist)
        return timelist

    def burnTime(self, balance_value, previous_amount):

        balance_date = None
        previous_balance = None
        next_balances = None
        prev_date = None

        for item in self.balance_list:
            if item[1] == balance_value:
                try:
                    balance_date = item[0]
                    previous_balance = mean([self.balance_list[self.balance_list.index(item) + i + 1][1] for i in range(previous_amount)])
                    prev_date = self.balance_list[self.balance_list.index(item) + 1][0]
                    next_balances = [x for x in reversed(self.balance_list[:self.balance_list.index(item)])]
                except Exception as e:
                    #print(item)
                    #print(e)
                    pass

        if balance_date is None or previous_balance is None or next_balances is None:
            raise Exception("Error de balance date o transaccion previa (self.burnRate())")

        if next_balances == []:
            return -1

        burnTime = -1

        for balance in next_balances:
            # print("hey1")

            if balance[1] <= previous_balance:
                # print("hey2")

                time_prev = [int(x) for x in prev_date.split("-")]
                # print(time_prev)
                time_prev = date(time_prev[0], time_prev[1], time_prev[2])

                time_post = [int(x) for x in balance[0].split("-")]
                #print(time_post)
                time_post = date(time_post[0], time_post[1], time_post[2])

                burnTime = time_post - time_prev
                break

        return burnTime

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
            min_value = min(balance_list)
            balance_list = [x - min_value for x in balance_list]

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

        #plt.figure(dpi = 1200)

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
                print(item["assets"])
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

timeseriesbyid("660ccd46-5b75-4478-b270-702b8cde06a2")

#timeseriesbyid("132531db-8216-4729-8c62-d1e65d14a187")
#timeseriesbyid("2ed76be0-0e12-41c5-aa00-e0dc7b3fd637")
#timeseriesbyid("8775f1e8-4f46-499b-873a-1568663c339f")
#timeseriesbyid("90c6fdec-74f5-4c48-99d3-a2cde6321c8c")
#timeseriesbyid("e05e3e20-7143-46ed-8e39-095c86fa7721")


def x_most_transactions(x):

    best_ids = {}

    for item in container:

        if len(best_ids) < x:
            best_ids[item["reportId"]] = len(item["transactions"])

        elif len(item["transactions"]) >= min(best_ids.values()):

            keu = None

            for key, value in best_ids.items():
                if value == min(best_ids.values()):

                    keu = key


            best_ids[item["reportId"]] = len(item["transactions"])
            del best_ids[keu]

    return best_ids

#print(x_most_transactions(5))

#timeseriesbyid(container[321]["reportId"])
#BalanceHistory(fake_report["reportId"], fake_report["transactions"], fake_report["assets"]["accounts"]["account1"]["balance"])
