
from querygen import querygen
import pickle
from parameters import bank

class Account(object):
    def __init__(self, reportId):
        self.reportId = reportId
        self.transactions = []
        self.freq_dict = None

    def addTransaction(self, transaction):
        self.transactions.append(['-'.join(transaction['date'].split('-')[:2]), transaction['description'], transaction['in'], transaction['out']])

    def displayAll(self):
        for transaction in self.transactions:
            print(transaction)

        print(" ")
        print(f"Transacciones Totales: {len(self.transactions)}")

    def genfreqdict(self):

        freq_dict = {}

        for transaction in self.transactions:
            for word in transaction[1].lower().split(' '):
                try:
                    freq_dict[word] += 1
                except KeyError:
                    freq_dict[word] = 1

        self.freq_dict = freq_dict

    def standarize(self, banks):

        """

        La generalizacion de descripciones es un supuesto

        """

        if banks == "santander":

            for item in self.transactions:
                if "transf" in item[1].lower():
                    item[1] = "Transferencia"
                elif "remuneracion" in item[1].lower():
                    item[1] = "Remuneracion"
                elif 'trasp' in item[1].lower():
                    item[1] = 'Traspaso'

        elif banks == 'falabella':
            for item in self.transactions:
                print(item)

        elif banks == 'bancodechile':
            for item in self.transactions:
                if 'transferencia' in item[1].lower():
                    item[1] = "Transferencia"
                elif 'traspaso' in item[1].lower():
                    item[1] = "Traspaso"
                elif 'sueldo' in item[1].lower():
                    item[1] = "Sueldo"

class AccountContainer(object):
    def __init__(self):
        self.accounts = []

    def add_account(self, account):
        self.accounts.append(account)

def duplicateFiltering(all_data):

    DataDict = {}

    for report in all_data:
        try:
            if len(report[1]) >= DataDict[report[0]]:
                DataDict[report[0]] = report[1]
        except:
            DataDict[report[0]] = report[1]

    return DataDict

def inoutFiltering(data_dict):

    for k in data_dict.keys():

        wanted_transactions = []

        for transaction in data_dict[k]:
            if transaction['in'] != 0:
                wanted_transactions.append(transaction)

        data_dict[k] = wanted_transactions[:]

    return data_dict

def accountGen(data_dict):

    all_accounts = AccountContainer()

    for k in data_dict.keys():
        temp_account = Account(k)

        for item in data_dict[k]:
            temp_account.addTransaction(item)

        temp_account.genfreqdict()
        temp_account.standarize(bank)
        all_accounts.add_account(temp_account)

    return all_accounts

def exportData(item, all_banks = False):

    if not all_banks:
        with open(f'Data/{bank}.pickle', 'wb') as outfile:
            pickle.dump(item, outfile)

    else:
        with open(f'Data/all_reports.pickle', 'wb') as infile:
            return pickle.dump(item, infile)

def importData(all_banks = False):

    if not all_banks:
        with open(f'Data/{bank}.pickle', 'rb') as infile:
            return pickle.load(infile)
    else:
        with open(f'../Data/all_reports.pickle', 'rb') as infile:
            return pickle.load(infile)


if __name__ == '__main__':

    with open("Data/all_data.pickle", "rb") as infile:
        container = pickle.load(infile)

    data = [[x["reportId"], x["transactions"]] for x in container if type(x) == dict and x["bank"] == "estado"]

    container = accountGen(inoutFiltering(duplicateFiltering(data)))

    #container = accountGen(duplicateFiltering(querygen(None)))

    exportData(container, all_banks=False)

    #container = importData()

    #container2 = accountGen(duplicateFiltering(data))

