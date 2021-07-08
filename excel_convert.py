
from accounts import importData, Account, AccountContainer
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from statistics import stdev, mean
from time import sleep

class Stats(object):
    def __init__(self):

        self.stats = {}
        self.general_stats = {'Total Reportes': 0}
        self.desc_dict = None
        self.account_dict = None

    def get_dict_stats(self):

        for key in self.desc_dict.keys():

            obj = self.desc_dict[key][1]

            try:
                stde = stdev(obj)
            except:
                stde = 0

            self.stats[key] = [self.desc_dict[key][0], round(mean(obj)), max(obj), min(obj), round(stde)]

    def get_account_stats(self):

        obj = [len(account) for account in self.account_dict.values()]

        self.general_stats['Reportes'] = len(self.account_dict)
        self.general_stats['Promedio'] = mean(obj)
        self.general_stats['Max'] = max(obj)
        self.general_stats['Min'] = min(obj)
        self.general_stats['STDEV'] = round(stdev(obj))

def openSheet():

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('infobancosauth.json', scope)

    client = gspread.authorize(creds)
    sheet = client.open('Estadisticas por Banco')

    return sheet.get_worksheet(1)  # Santander

def obtenerStats(contenedor):

    stats = Stats()
    desc_dict = {}
    account_dict = {}

    for account in contenedor.accounts:
        stats.general_stats['Total Reportes'] += 1
        account.standarize_Santander()  #Remover al re-crear cuentas

        account_dict[account.consumerId] = []

        for item in account.transactions:

            account_dict[account.consumerId].append(item)

            try:
                amount = float(f"{item[2]}")

                try:
                    # description: [quantity, [amount1, amount2, ...]]

                    desc_dict[item[1]][0] += 1  # desc_dict[description][quantity]
                    desc_dict[item[1]][1].append(amount)  # desc_dict[description][amount_list]
                except:
                    desc_dict[item[1]] = [1, [amount]]

            except:
                pass

    stats.desc_dict = desc_dict
    stats.account_dict = account_dict

    stats.get_dict_stats()
    stats.get_account_stats()

    return stats

def statsToSheet(sheetInstance, stat):

    count = 5    #Desface Row
    for key, values in stat.stats.items():
        sheetInstance.update_cell(count, 2, key)
        sleep(5)

        iterator = 3   #Desface Col
        for val in values:
            sheetInstance.update_cell(count, iterator, val)
            iterator += 1

        count += 1

    sheetInstance.update_cell(3, 11, stat.general_stats['Reportes'])
    sheetInstance.update_cell(4, 11, stat.general_stats['Promedio'])
    sheetInstance.update_cell(5, 11, stat.general_stats['Max'])
    sheetInstance.update_cell(6, 11, stat.general_stats['Min'])
    sheetInstance.update_cell(7, 11, stat.general_stats['STDEV'])


if __name__ == '__main__':

    container = importData()

    worksheet = openSheet()
    statsToSheet(worksheet, obtenerStats(container))
