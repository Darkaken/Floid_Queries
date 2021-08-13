
#table_name = "backoffice-dev-reports"

table_name = "dashboard-prod-reports"
bank = 'estado'

min_transaction_quantity = 5

trash_filters = [
    "status == OK",
    "country == CO",
]

query_filters = [
    #f"bank == {bank}",
]

complex_filters = [

    #[func attr_name operator value]

    f"size transactions >= {min_transaction_quantity}",
]

##### CONSTANTS #####

operatorConversionDict = {
    "==": "eq",
    ">=": "gte"
}

