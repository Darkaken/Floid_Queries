
import pickle
import matplotlib.pyplot as plt
from datetime import date, datetime, timedelta
import math
from statistics import mean
import re

from parameters import high_income_words, low_income_words, investment_words, not_income_words

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


def encontrar_empleador(reporte, palabras_empleador, N = 2, valor_min = 50000):

    income_transactions = []
    candidatos = []
    candidatos_unique = {}

    for transaction in reporte['transactions']:
        try:
            if transaction['in'] > valor_min:
                income_transactions.append(transaction)
        except:
            pass

    for transaction in income_transactions:
        found = False
        desc = transaction['description'].lower()

        for word in palabras_empleador:
            if (' ' + word) in desc or (word + ' ') in desc:
                found = True
                candidatos.append(transaction)
                break

        if not found:
            if len(re.sub("[^0-9]", "", desc)) >= 7: #Si es que tiene mas de 7 numeros asumimos que es un rut
                candidatos.append(transaction)
                break

    for transaction in candidatos:
        if sum([1 for x in candidatos if x['description'] == transaction['description']]) >= N:
            try:
                candidatos_unique[transaction['description']].append(transaction['in'])
            except:
                candidatos_unique[transaction['description']] = [transaction['in']]

    final_candidatos = []

    for k, v in candidatos_unique.items():
        final_candidatos.append([k, round(mean(v))])

    try:
        #print(final_candidatos)
        return [x[0] for x in final_candidatos if x[1] == max([value[1] for value in final_candidatos])]
    except:
        return []

def encontrar_dependencia_primer_algoritmo(reporte, palabras_clave_high, palabras_clave_low, valor_min = 50000):

    high_income_transactions = []
    low_income_transactions = []
    income_transactions = []

    for transaction in reporte['transactions']:
        try:
            if transaction['in'] > valor_min:
                income_transactions.append(transaction)
        except:
            pass

    for transaction in income_transactions:

        desc = transaction['description'].lower()

        if len(re.sub("[^0-9]", "", desc)) >= 7:
            high_income_transactions.append(transaction)
        elif "remuneracion" in desc:
            high_income_transactions.append(transaction)
        elif "sueldo" in desc:
            high_income_transactions.append(transaction)
        elif "trabajo" in desc:
            high_income_transactions.append(transaction)
        else:
            if "spa" in desc:
                low_income_transactions.append(transaction)

    found = False
    confidence = 'None'

    if len(high_income_transactions) > 0:
        found = True
        confidence = 'High'
    elif len(low_income_transactions) > 0:
        found = True
        confidence = 'Low'

    return [found, confidence]

def encontrar_dependencia_segundo_algoritmo(reporte, X, P, N, U, T, Q, B):

    #TIPO I

    min_meses = X
    porcentaje_ingreso = P
    frecuecia_minima = N
    desviacion_de_maximos = U
    diferencia_mensual = T

    #TIPO II

    desviacion_balance = Q
    cantidad_minima_transacciones = B

    income_transactions = []

    for transaction in reporte['transactions']:
        try:
            if transaction['in'] > 0:
                income_transactions.append(transaction)
        except:
            pass


def encontrar_ingreso(reporte, N, len_burnout):

    valor_min = N

    high_income_transactions = []
    low_income_transactions = []
    income_transactions = []

    not_income_transactions = []

    for transaction in reporte['transactions']:
        try:
            if transaction['in'] >= valor_min:
                income_transactions.append(transaction)
        except:
            pass

    for transaction in income_transactions:

        desc = transaction['description'].lower()

        if len(re.sub("[^0-9]", "", desc)) >= 7:
            high_income_transactions.append(transaction)
        else:

            isIncome = False
            for keyword in high_income_words:
                if keyword in desc:
                    high_income_transactions.append(transaction)
                    isIncome = True

            for keyword in low_income_words:
                if keyword in desc:
                    low_income_transactions.append(transaction)
                    isIncome = True

            if not isIncome:
                not_income_transactions.append(transaction)

    high_confidence_income = sum(transaction['in'] for transaction in high_income_transactions) / len_burnout
    low_confidence_income = sum(transaction["in"] for transaction in low_income_transactions) / len_burnout

    not_income_transactions_filtered = not_income_transactions[:]

    not_words = investment_words + not_income_words
    for transaction in not_income_transactions:
        for keyword in not_words:
            if keyword in transaction['description'].lower():
                try:
                    not_income_transactions_filtered.remove(transaction)
                except:
                    pass

    no_confidence_income = sum(transaction['in'] for transaction in not_income_transactions) / len_burnout

    for transaction in high_income_transactions:
        print(f"high {transaction['description']} : {transaction['in']}")

    print("")
    for transaction in low_income_transactions:
        print(f"low {transaction['description']} : {transaction['in']}")

    print("")
    for transaction in not_income_transactions_filtered:
        print(f"none {transaction['description']} : {transaction['in']}")

    print("")

    print(f' High Confidence: {round(high_confidence_income)}')
    print(f' Low Confidence: {round(low_confidence_income)}')
    print(f' Total Income: {round(float(high_confidence_income) + float(low_confidence_income))}')

    print("")
    print(f' No Confidence: {round(no_confidence_income)}')


    return [high_confidence_income, low_confidence_income, not_income_transactions_filtered]

def incomeseries(not_income_transactions_filtered):

    pass


def test(all_reports):

    stat_dict = {
        'all_reports': len(all_reports),
        'dependiente_alto': 0,
        'dependiente_bajo': 0,
        'independiente': 0,
        'found_empleador': 0,
        'empleador_not_found': 0
    }

    for item in all_reports:
        if encontrar_empleador(item, ['spa'], 2) != []:
            stat_dict['found_empleador'] += 1
        else:
            stat_dict['empleador_not_found'] += 1

        found, confidence = encontrar_dependencia_primer_algoritmo(item, [], [])

        if found:
            if confidence == 'High':
                stat_dict['dependiente_alto'] += 1
            else:
                stat_dict['dependiente_bajo'] += 1
        else:
            stat_dict['independiente'] += 1

    print(stat_dict)
    return stat_dict

def income_test(report):

    burn_rate_matrix = timeseriesbyid(report['reportId'])

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

        result = encontrar_ingreso(report, 25000, len(burn_rate_matrix) - 1)

        return result

    print(burn_rate_matrix)


with open("Data/all_data.pickle", "rb") as infile:
    container = pickle.load(infile)

    number = 2643

    result = income_test(container[number])

    print('')
    print(f' Main Income: {container[number]["income"]["mainAverage"]}')
    print(f" Total Income: {container[number]['income']['totalAverage']}")


# 2643
# 315
# 2771
# 3542
# 4162

#Valor minimo de transaccion

#palabras_high_income
#palabras_low_income
#palabras_investment
#palabras_not_income

#representa_X_percent_income_total
#porcentaje_de_pendiente_a_considerar