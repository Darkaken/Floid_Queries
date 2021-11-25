
import pickle
import matplotlib.pyplot as plt
from datetime import date, datetime, timedelta
import math
import re

from timeseries import BalanceHistory, timeseriesbyid

def roundup(x):
    return int(math.ceil(x / 100.0)) * 100


def ammount_of_transactions(all_reports):

    return_dict = {}

    for item in [x for x in range(0, 2500, 100)]:
        return_dict[item] = 0

    for report in all_reports:
        return_dict[roundup(len(report["transactions"]))] += 1

    plt.plot(return_dict.values(), return_dict.keys(), 'ro')
    plt.xlabel("Cantidad de Reportes")
    plt.ylabel("Cantidad de Transacciones Totales")
    plt.show()

    return return_dict

def ammount_of_in_transactions(all_reports):

    return_dict = {}

    for item in [x for x in range(0, 2500, 100)]:
        return_dict[item] = 0

    i = 0
    for report in all_reports:
        try:
            return_dict[roundup(len([0 for x in report['transactions'] if x['in'] > 0]))] += 1
        except:
            i += 1

    print(f'Cantidad de reportes sin transacciones entrantes: {i}')

    plt.plot(return_dict.values(), return_dict.keys(), 'ro')
    plt.xlabel("Cantidad de Reportes")
    plt.ylabel("Cantidad de Transacciones de Ingreso")
    plt.show()

    return return_dict

def ammount_of_out_transactions(all_reports):
    return_dict = {}

    for item in [x for x in range(0, 2500, 100)]:
        return_dict[item] = 0

    i = 0
    for report in all_reports:
        try:
            return_dict[roundup(len([0 for x in report['transactions'] if x['out'] > 0]))] += 1
        except:
            i += 1

    print(f'Cantidad de reportes sin transacciones salientes: {i}')

    plt.plot(return_dict.values(), return_dict.keys(), 'ro')
    plt.xlabel("Cantidad de Reportes")
    plt.ylabel("Cantidad de Transacciones de Egreso")
    plt.show()

    return return_dict

def reports_by_bank(all_reports):

    return_dict = {}

    for report in all_reports:
        try:
            return_dict[report['bank']] += 1
        except:
            return_dict[report['bank']] = 1

    plt.bar(return_dict.keys(), return_dict.values())
    plt.xlabel("Banco")
    plt.ylabel("Cantidad de Reportes")
    plt.xticks(fontsize = 7)

    plt.show()

    return return_dict

def distribucion_de_ingreso_por_banco(all_reports, bice = True):

    return_dict = {}
    bank_list = []

    for report in all_reports:
        try:
            return_dict[report['bank']][0] += 1
            try:
                return_dict[report['bank']][1] += sum(x['in'] for x in report['transactions'] if x['in'] > 0)
            except:
                pass
        except:
            try:
                return_dict[report['bank']] = [1, sum(x['in'] for x in report['transactions'] if x['in'] > 0)]
                bank_list.append(report['bank'])
            except:
                pass

    for item in bank_list:
        return_dict[item] = round(return_dict[item][1] / return_dict[item][0]) /12

    if not bice:
        del return_dict['bice']

    plt.bar(return_dict.keys(), return_dict.values())
    plt.xlabel("Banco")
    plt.ylabel("Ingreso Promedio")
    plt.xticks(fontsize = 7)

    plt.show()

    return return_dict

def distribucion_de_gasto_por_banco(all_reports, bice = True):

    return_dict = {}
    bank_list = []

    for report in all_reports:
        try:
            return_dict[report['bank']][0] += 1
            try:
                return_dict[report['bank']][1] += sum(x['out'] for x in report['transactions'] if x['out'] > 0)
            except:
                pass
        except:
            try:
                return_dict[report['bank']] = [1, sum(x['out'] for x in report['transactions'] if x['out'] > 0)]
                bank_list.append(report['bank'])
            except:
                pass

    for item in bank_list:
        return_dict[item] = round(return_dict[item][1] / return_dict[item][0]) / 12

    if not bice:
        del return_dict['bice']

    plt.bar(return_dict.keys(), return_dict.values())
    plt.xlabel("Banco")
    plt.ylabel("Gasto Promedio")
    plt.xticks(fontsize = 7)

    plt.show()

    return return_dict

def avg_transaction_by_bank(all_reports, mode):

    if mode == "in":
        generate_avg_transactions(all_reports, 'in')
    elif mode == "out":
        generate_avg_transactions(all_reports, 'out')
    elif mode == "all":
        generate_avg_transactions(all_reports, 'all')
    else:
        return -3 #wrong input

def generate_avg_transactions(all_reports, mode):
    return_dict = {}
    bank_list = []

    if mode == 'out' or mode == 'in':
        for report in all_reports:
            try:
                return_dict[report['bank']][0] += 1
                try:
                    return_dict[report['bank']][1] += len([x for x in report['transactions'] if x[mode] > 0])
                except:
                    pass
            except:
                try:
                    return_dict[report['bank']] = [1, len([x for x in report['transactions'] if x[mode] > 0])]
                    bank_list.append(report['bank'])
                except:
                    pass

    elif mode == 'all':
        for report in all_reports:
            try:
                return_dict[report['bank']][0] += 1
                try:
                    return_dict[report['bank']][1] += len([x for x in report['transactions']])
                except:
                    pass
            except:
                try:
                    return_dict[report['bank']] = [1, len([x for x in report['transactions']])]
                    bank_list.append(report['bank'])
                except:
                    pass

    for item in bank_list:
        return_dict[item] = round(return_dict[item][1] / return_dict[item][0])


    if mode == 'in':
        mode = 'de Ingreso'
    elif mode == 'out':
        mode = 'de Gasto'
    elif mode == 'all':
        mode = ''

    plt.bar(return_dict.keys(), return_dict.values())
    plt.xlabel("Banco")
    plt.ylabel(f"Cantidad de Transacciones {mode} Promedio")
    plt.xticks(fontsize=7)

    plt.show()

    return return_dict

############### REPORT SPECIFIC ##################

def encontrar_ahorro_inversion(one_report, len_burnout):

    total_ahorro = 0

    outcome_transactions = []

    for transaction in one_report['transactions']:
        try:
            if transaction['out']:
                outcome_transactions.append(transaction)
        except:
            pass

    for transaction in outcome_transactions:

        desc = transaction['description'].lower()

        if 'ahorro' in desc:
            total_ahorro += transaction['out']
        elif 'inversion' in desc:
            total_ahorro += transaction['out']
        elif 'fintual' in desc:
            total_ahorro += transaction['out']
        elif 'fondos' in desc:
            total_ahorro += transaction['out']
        elif 'mutuos' in desc:
            total_ahorro += transaction['out']

    return round(total_ahorro / len_burnout)

def encontrar_empresas_en_ingresos(one_report, N, len_burnout):

    high_income_transactions = []
    low_income_transactions = []

    income_transactions = []
    empresa = None

    for transaction in one_report['transactions']:
        try:
            if transaction['in'] > N:
                income_transactions.append(transaction)
        except:
            pass

    for transaction in income_transactions:

        desc = transaction['description'].lower()

        if "spa" in desc:
            low_income_transactions.append(transaction)
        elif "remuneracion" in desc:
            high_income_transactions.append(transaction)
        elif "sueldo" in desc:
            high_income_transactions.append(transaction)
        elif "trabajo" in desc:
            high_income_transactions.append(transaction)
        else:
            for char in desc:
                if char in "0123456789-":
                    low_income_transactions.append(transaction)
                    break

    ########### filtrar ############

    ingreso_high = 0
    ingreso_low = 0

    if len(high_income_transactions) != 0:
        empresa = [x['description'] for x in high_income_transactions if x['in'] == max([y['in'] for y in high_income_transactions])][0]

    try:
        for transaction in high_income_transactions:
            if word_filter(transaction['description'].lower()):
                ingreso_high += transaction['in']

        ingreso_high /= len_burnout

    except:
        ingreso_high = 0

    try:
        for transaction in low_income_transactions:
            if word_filter(transaction['description'].lower()):
                ingreso_low += transaction['in']

        ingreso_low /= len_burnout
    except:

        ingreso_low = 0

    return empresa, round(ingreso_high), round(ingreso_low)

def word_filter(word):

    if 'propia' in word:
        return False

    elif 'afp' in word:
        return False

    elif 'MI 10' in word:
        return False
    elif '10' in word:
        return False

    return True

def get_all_stats(one_report):

    stat_dict = {
        'burn_rate_matrix': None,
        'empresa_ingreso': None,
        'dependiente': False,
        'ingreso_high': None,
        'ingreso_low': None,
        'ahorro': 0
    }

    burn_rate_matrix = timeseriesbyid(one_report['reportId'])

    if burn_rate_matrix != -1 and burn_rate_matrix is not None:
        burn_rate_matrix = [x for x in burn_rate_matrix if type(x) == list]

        try:
            max_len = max([len(x) for x in burn_rate_matrix])
        except:
            pass

        try:
            for item in burn_rate_matrix:
                for i in range(max_len - len(item)):
                    item.append('inf')
        except:
            pass

        stat_dict['burn_rate_matrix'] = burn_rate_matrix

    try:
        stat_dict['empresa_ingreso'], stat_dict['ingreso_high'], stat_dict['ingreso_low'] = encontrar_empresas_en_ingresos(one_report, 50000, len(burn_rate_matrix) - 1)
    except:
        None

    if stat_dict['empresa_ingreso'] is not None:
        stat_dict['dependiente'] = True

    try:
        stat_dict['ahorro'] += encontrar_ahorro_inversion(one_report, len(burn_rate_matrix) - 1)
    except:
        pass

    return stat_dict


def test(all_reports):

    stat_dict = {
        'all_reports': len(all_reports),
        'burn_rate_matrix': 0,
        'empresa_ingreso': 0,
        'dependiente': 0,
        'ingreso_high': 0,
        'ingreso_low': 0,
        'ahorro': 0,
        'independiente': 0,
    }

    for item in all_reports:
        datas = get_all_stats(item)

        for key in datas.keys():
            if datas[key]:
                stat_dict[key] += 1

    stat_dict['independiente'] = len(all_reports) - stat_dict['dependiente']

    print(stat_dict)
    return stat_dict


with open("Data/all_data.pickle", "rb") as infile:
    container = pickle.load(infile)

    test(container)
    #data = get_all_stats(container[2888])
    #print(container[2888]['reportId'])

    #print(data)