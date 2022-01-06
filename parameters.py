
#table_name = "backoffice-dev-reports"

table_name = "dashboard-prod-reports"
bank = 'estado'

min_transaction_quantity = 5

trash_filters = [
    "status == OK",
    "country == CL",
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

##### METRICS #####

high_income_words = ["ingreso", "remuneracion", "sueldo", "trabajo", 'ife']
low_income_words = ["spa", "deposito", "efectivo", "sociedad", "fundacion", "solidario", "ingenieria"]

investment_words = ["ahorro", "inversion", "fintual", "fondos", "mutuos", "rescate", "acciones"]
not_income_words = ['diez', 'modelo', 'porciento', "afp"]

#NOTA: IFE APARTE + SOLIDARIO
#Recurrencia: 3 Meses minimo



