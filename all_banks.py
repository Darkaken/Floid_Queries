
from querygen import querygen
from accounts import duplicateFiltering


bank_list = [
    "bci",
    "santander",
    "falabella",
    "ripley",
    "scotiabank",
    "bancodechile",
    "estado",
    "bancolombia"
]

value_dict = {}

for bank in bank_list:
    query_filters = [f"bank == {bank}"]
    value_dict[bank] = len(duplicateFiltering(querygen(query_filters)))

print(value_dict)
