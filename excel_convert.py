
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

def merger(containers):

    result = {}
    for account in containers.accounts:
        result = mergeDicts(result, account.freq_dict)

    return result

def mergeDicts(dict1, dict2):

    result = {}

    for key in dict1.keys():
        try:
            result[key] += dict1[key]
        except KeyError:
            result[key] = dict1[key]

    for key in dict2.keys():
        try:
            result[key] += dict2[key]
        except KeyError:
            result[key] = dict2[key]

    return result


def openSheet():

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('infobancosauth.json', scope)

    client = gspread.authorize(creds)
    sheet = client.open('Estadisticas por Banco')

    return sheet.get_worksheet(2)

def obtenerStats(contenedor):

    stats = Stats()
    desc_dict = {}
    account_dict = {}

    for account in contenedor.accounts:
        stats.general_stats['Total Reportes'] += 1

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

    count = 2    #Desface Row
    for key, values in stat.stats.items():
        sheetInstance.update_cell(count, 2, key)
        sleep(5)

        iterator = 1  #Desface Col
        for val in values:
            sheetInstance.update_cell(count, iterator, val)
            iterator += 1

        count += 1

    sheetInstance.update_cell(1, 11, stat.general_stats['Reportes'])
    sheetInstance.update_cell(2, 11, stat.general_stats['Promedio'])
    sheetInstance.update_cell(3, 11, stat.general_stats['Max'])
    sheetInstance.update_cell(4, 11, stat.general_stats['Min'])
    sheetInstance.update_cell(5, 11, stat.general_stats['STDEV'])

def getFrecuency(freq_dict):
    new_dict = {}

    all_words = sum([x for x in freq_dict.values()])

    for key in freq_dict.keys():
        num = freq_dict[key]
        new_dict[key] = [num, num/all_words]

    return new_dict

def frecuencyToSheet(sheetInstance, freq_dict):

    freq_dict = getFrecuency(freq_dict)

    count = 2   #Desface Row
    column = 13  #Desface Col
    for key in freq_dict.keys():

        if freq_dict[key][0] < 5:
            pass
        else:
            sleep(1)
            sheetInstance.update_cell(count, column, key)
            sleep(1)
            sheetInstance.update_cell(count, column + 1, freq_dict[key][0])
            sleep(1)
            sheetInstance.update_cell(count, column + 2, freq_dict[key][1])

            count += 1


if __name__ == '__main__':

    container = importData()

    worksheet = openSheet()
    frecuencyToSheet(worksheet, merger(container))
    statsToSheet(worksheet, obtenerStats(container))
