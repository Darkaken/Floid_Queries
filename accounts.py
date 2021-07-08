
from querygen import querygen
import pickle

class Account(object):
    def __init__(self, consumerId):
        self.consumerId = consumerId
        self.transactions = []

    def addTransaction(self, transaction):
        self.transactions.append(['-'.join(transaction['date'].split('-')[:2]), transaction['description'], transaction['in']])

    def displayAll(self):
        for transaction in self.transactions:
            print(transaction)

    def standarize_Santander(self):

        """

        La generalizacion de descripciones es un supuesto

        """

        for item in self.transactions:
            if "Transf" in item[1]:
                item[1] = "Transferencia"
            elif "REMUNERACION" in item[1]:
                item[1] = "Remuneracion"
            elif 'Trasp' in item[1]:
                item[1] = 'Traspaso'

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

        temp_account.standarize_Santander()     #Especifico Para Santander
        all_accounts.add_account(temp_account)

    return all_accounts

def exportData(item):

    with open('Data/account_data_full', 'wb') as outfile:
        pickle.dump(item, outfile)

def importData():

    with open('Data/account_data_full', 'rb') as infile:
        return pickle.load(infile)


if __name__ == '__main__':

    pass
    #container = accountGen(inoutFiltering(duplicateFiltering(querygen())))
    #exportData(container)

    container = importData()

    print(len(container.accounts))



