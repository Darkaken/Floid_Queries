
#table_name = "backoffice-dev-reports"

table_name = "dashboard-prod-reports"


min_transaction_quantity = 5

trash_filters = [
    "status == OK",
    "country == CL",
]

query_filters = [
    "bank == santander"
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

