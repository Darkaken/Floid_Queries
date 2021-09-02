
import parameters, boto3
from boto3.dynamodb.conditions import Key, Attr
from parameters import operatorConversionDict as ConvD
from time import sleep
import pickle

class QueryCreator(object):
    def __init__(self):
        self.query = None; self.table = None
        self.filters = []
        self.complex_filters = []

        self.query = ''

    def setAll(self, params, query_filter_override):

        self.setTableData(params.table_name)
        self.setTrashFilters(params.trash_filters)

        if query_filter_override is not None:
            self.setQueryFilters(query_filter_override)
        else:
            self.setQueryFilters(params.query_filters)

        self.setComplexFilters(params.complex_filters)

        self.create_filters()
        print(self.query)

    def create_filters(self):
        filters = ""

        for statement in self.filters:
            statement = statement.split(" ")

            filters += f"Attr('{statement[0]}').{ConvD[statement[1]]}('{statement[2]}') & "

        for statement in self.complex_filters:
            statement = statement.split(" ")

            filters += f"Attr('{statement[1]}').{statement[0]}().{ConvD[statement[2]]}({statement[3]}) & "

        self.query += filters[:-3]

    ## SETTER FUNCTIONS

    def setTableData(self, table_name):
        self.table = table_name

    def setTrashFilters(self, filters):
        for statement in filters:
            self.filters.append(statement)

    def setQueryFilters(self, filters):
        for statement in filters:
            self.filters.append(statement)

    def setComplexFilters(self, filters):
        for statement in filters:
            self.complex_filters.append(statement)

def querygen(query_filter_override):

    #All queries include unilimited pagination

    data = []

    QC = QueryCreator()

    if query_filter_override is not None:
        QC.setAll(parameters, query_filter_override)
    else:
        QC.setAll(parameters, None)

    dynamodb = boto3.resource("dynamodb", region_name = "sa-east-1")
    table = dynamodb.Table(QC.table)

    response = table.scan(
        FilterExpression = eval(QC.query)
    )

    for item in response["Items"]:
        data.append(item)                                          #For Stats.py

    #while False:
    while 'LastEvaluatedKey' in response:

        key = response['LastEvaluatedKey']

        while True:
            try:
                response = table.scan(
                    FilterExpression = eval(QC.query),
                    ExclusiveStartKey = key
                )
                print("success")
                break
            except:
                print('failed')

        for item in response["Items"]:
            data.append(item)                                      #For Stats.py

    return data
 

if __name__ == '__main__':

    item = querygen(None)
    print(len(item))

    with open(f'Data/all_data.pickle', 'wb') as infile:
        pickle.dump(item, infile)


""" 

Notes:

KeyConditionExpression: Only partition and sort key attributes
FilterExpression: Not partition nor sort key attributes
ExclusiveStartKey: Key marker for query position


"""


