import pandas as pd
import numpy as np
import ujson


# import pprint

# pp = pprint.PrettyPrinter(width=180, indent=4)


def also_bought(dataframe):
    '''

    :param dataframe: the dataframe of metadata
    :return: transactions of itmes bought together
    '''
    raw_transaction = {}

    for row in dataframe.itertuples():
        json_acceptable_string = row.related.replace("'", "\"")
        d = ujson.loads(json_acceptable_string)

        raw_transaction.setdefault(row.productID, d)

    transaction = []

    # pp.pprint(raw_transaction)
    for product in raw_transaction:
        bought_record = []
        if not 'also_bought' in raw_transaction[product]:
            continue
        raw_data = raw_transaction[product]['also_bought']
        for item in raw_data:
            if item in raw_transaction:
                bought_record.append(item
                                     )
        if bought_record:
            transaction.append(bought_record)
    return transaction


def also_viewed(dataframe):
    '''

      :param dataframe: the dataframe of metadata
      :return: transactions of itmes viewed together
    '''
    raw_transaction = {}

    for row in dataframe.itertuples():
        json_acceptable_string = row.related.replace("'", "\"")
        d = ujson.loads(json_acceptable_string)

        raw_transaction.setdefault(row.productID, d)

    viewed = []
    for product in raw_transaction:
        view_record = []
        if not 'also_viewed' in raw_transaction[product]:
            continue
        raw_data = raw_transaction[product]['also_viewed']
        for item in raw_data:
            if item in raw_transaction:
                view_record.append(item
                                   )
        if view_record:
            viewed.append(view_record)
    return viewed


if __name__ == '__main__':
    raw_meta = pd.read_csv('data/sample_data_meta.csv', index_col=0)

    print(also_viewed(raw_meta))
    print(also_bought(raw_meta))
