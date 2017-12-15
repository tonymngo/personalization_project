import pandas as pd
import numpy as np
import csv
import pprint
import pyfpgrowth

pp = pprint.PrettyPrinter(width=300, indent=4)


def generate_rules(dataframe, minsupport=25, minconfidence=0.55, satisfied_value=3):
    '''

    :param dataframe: it should includes userID, productID, rating
    :param minsupport: the itemset at least show up minsupport times
    :param minconfidence: the min possibility that the consumer will apply the rules
    :param satisified_value:  consider the user like the product only he rating it over the value
    :return:
    '''

    raw_dict = {}
    raw_recommendation = {}
    recommendation_dict = {}

    # transform dataframe to transaction
    for row in dataframe.itertuples():
        raw_dict.setdefault(row.reviewerID, {})
        if float(row.rating) >= satisfied_value:
            raw_dict[row.reviewerID].update({row.productID: row.rating})

    transaction = []
    for user in raw_dict:
        transaction.append(list(raw_dict[user].keys()))
    pp.pprint(transaction)
    pp.pprint(len(transaction))
    # generate the rules
    patterns = pyfpgrowth.find_frequent_patterns(transaction, minsupport)
    rules = pyfpgrowth.generate_association_rules(patterns, minconfidence)
    return rules

    # generate the raw recommendation
    # for user in raw_dict:
    #
    #     j = 0
    #     for item in rules:
    #         if all(i in raw_dict[user] for i in item) and any(i not in raw_dict[user] for i in rules[item][0]):
    #             raw_recommendation[user] = {'rule': [], 'recommendation': {}}
    #             raw_recommendation[user]['rule'].append(j)
    #             for recommendation in filter(lambda x: x not in raw_recommendation[user], rules[item][0]):
    #                 raw_recommendation[user]['recommendation'].update({recommendation: rules[item][1]})
    #
    #         j += 1
    # generate the final output
    # for user in raw_recommendation:
    #     recommendation_dict[user] = sorted(raw_recommendation[user]['recommendation'],
    #                                        key=raw_recommendation[user]['recommendation'].get,
    #                                        reverse=True)
    # return recommendation_dict


def predict(dataframe, rules):
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
    # satisfied_value = 1
    #
    # dict_ = {}
    # with open('data/sample_data.csv', 'r') as csvfile:
    #     spamreader = csv.reader(csvfile, delimiter=',')
    #     for row in spamreader:
    #         if row[0] == '':
    #             continue
    #         dict_.setdefault(row[1], {})
    #         if float(row[3]) > satisfied_value:
    #             dict_[row[1]].update({row[2]: True})
    #         else:
    #             dict_[row[1]].update({row[2]: False})
    #
    # pp.pprint(dict_)
    # dataframe = pd.DataFrame.from_dict(dict_)
    #
    # for user in dict_:
    #     pprint(dataframe[user])
    #
    # transaction = []
    # for user in dict_:
    #     transaction.append(list(dict_[user].keys()))
    # pp.pprint(transaction)
    # patterns = pyfpgrowth.find_frequent_patterns(transaction, 10)
    # rules = pyfpgrowth.generate_association_rules(patterns, 0.55)
    # pp.pprint(rules)
    # item_list = [key for key in rules]
    #
    # pp.pprint(item_list)
    # user_dict = {}
    #
    # for user in dict_:
    #     for item in dict_[user]:
    #         pp.pprint(item)
    # if item in item_list:
    #     i += 1
    # break

    # pp.pprint(i)
    # for item in item_list:
    #
    #     pp.pprint(rules[item])

    # for user in dict_:
    #
    #     j = 0
    #     for item in item_list:
    #         if all(i in dict_[user] for i in item) and any(i not in dict_[user] for i in rules[item][0]):
    #             user_dict[user] = {'rule': [], 'recommendation': {}}
    #             user_dict[user]['rule'].append(j)
    #             for recommendation in filter(lambda x: x not in dict_[user], rules[item][0]):
    #                 user_dict[user]['recommendation'].update({recommendation: rules[item][1]})
    #
    #         j += 1
    #
    # pp.pprint(len(user_dict))
    # pp.pprint(user_dict)
    #
    # result = {}
    #
    # for user in user_dict:
    #     result[user] = sorted(user_dict[user]['recommendation'], key=user_dict[user]['recommendation'].get,
    #                           reverse=True)
    #
    # pp.pprint(result)
    # pp.pprint(len(result))
    dt = pd.read_csv('data/sample_data.csv', index_col=0)  #
    rule = generate_rules(dt, minsupport=25)
    pp.pprint(rule)
    recommendation = predict(dt,rule)
    pp.pprint(recommendation)
    pp.pprint(len(recommendation))
