import association_model
import deal_meta
import pandas as pd

if __name__ == '__main__':
    trainset = pd.read_csv('data/sample_data.csv', index_col=0)
    metadata = pd.read_csv('data/sample_data_meta.csv', index_col=0)

    # it all return list
    bought_together = deal_meta.also_bought(metadata)
    view_together = deal_meta.also_viewed(metadata)

    # merge this two list
    bought_together.extend(view_together)
    # get the rule
    rule = association_model.generate_rules(trainset, information=bought_together, minsupport=25, minconfidence=0.55)
    # get the recommendation
    recommendation = association_model.predict(trainset, rules=rule)
    print(recommendation)
