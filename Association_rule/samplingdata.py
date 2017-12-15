import pandas as pd
import numpy as np
import ujson

import pprint

pp = pprint.PrettyPrinter(width=180, indent=4)

if __name__ == '__main__':
    # dt = pd.read_csv('data/sample_data.csv', index_col=0)
    # item_dict = {}

    # transform dataframe to transaction
    # for row in dt.itertuples():
    #     item_dict.setdefault(row.productID, None)

    # pp.pprint(item_dict)


    raw_meta = pd.read_csv('data/sample_data_meta.csv', index_col=0)
    raw_transaction = {}

    for row in raw_meta.itertuples():
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

    pp.pprint(transaction)
    pp.pprint(len(transaction))
    also_viewed = []
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
            also_viewed.append(view_record)
    pp.pprint(also_viewed)
    pp.pprint(len(also_viewed))








    # for item in data:
    #     pp.pprint(item)


    # for line in data:
    #     pprint(line)
