import pandas as pd
# import pprint
import pyfpgrowth

# pp = pprint.PrettyPrinter(width=300, indent=4)


def generate_rules(dataframe, information=[], minsupport=25, minconfidence=0.55, satisfied_value=3):
    '''
    :param information: the transaction we already have
    :param dataframe: it should includes userID, productID, rating
    :param minsupport: the itemset at least show up minsupport times
    :param minconfidence: the min possibility that the consumer will apply the rules
    :param satisified_value:  consider the user like the product only he rating it over the value
    :return: rules: the association rules
    '''

    raw_dict = {}

    # transform dataframe to transaction
    for row in dataframe.itertuples():
        raw_dict.setdefault(row.reviewerID, {})
        if float(row.rating) >= satisfied_value:
            raw_dict[row.reviewerID].update({row.productID: row.rating})

    transaction = []
    for user in raw_dict:
        transaction.append(list(raw_dict[user].keys()))
    if information:
        transaction.extend(information)

    # pp.pprint(transaction)
    # pp.pprint(len(transaction))


    # generate the rules
    patterns = pyfpgrowth.find_frequent_patterns(transaction, minsupport)
    rules = pyfpgrowth.generate_association_rules(patterns, minconfidence)
    return rules


def predict(dataframe, rules):
    '''

    :param dataframe: the trainset data
    :param rules: the association rule
    :return:  the recommended product
    '''
    raw_dict = {}
    raw_recommendation = {}
    recommendation_dict = {}
    # transform dataframe to transaction
    for row in dataframe.itertuples():
        raw_dict.setdefault(row.reviewerID, {})
        raw_dict[row.reviewerID].update({row.productID: row.rating})

    # generate the raw recommendation
    for user in raw_dict:

        j = 0
        for item in rules:
            if all(i in raw_dict[user] for i in item) and any(i not in raw_dict[user] for i in rules[item][0]):
                raw_recommendation[user] = {'rule': [], 'recommendation': {}}
                raw_recommendation[user]['rule'].append(j)
                for recommendation in filter(lambda x: x not in raw_recommendation[user], rules[item][0]):
                    raw_recommendation[user]['recommendation'].update({recommendation: rules[item][1]})
            j += 1

    # generate the final output
    for user in raw_recommendation:
        recommendation_dict[user] = sorted(raw_recommendation[user]['recommendation'],
                                           key=raw_recommendation[user]['recommendation'].get,
                                           reverse=True)
    return recommendation_dict


if __name__ == '__main__':
    dt = pd.read_csv('data/sample_data.csv', index_col=0)  #
    rule = generate_rules(dt, minsupport=25)
    # pp.pprint(rule)
    recommendation = predict(dt, rule)
    print(recommendation)
    print(len(recommendation))
