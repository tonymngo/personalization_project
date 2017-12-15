import csv
import pprint

pp = pprint.PrettyPrinter(width=180, indent=4)

if __name__ == '__main__':

    dict_ = {}
    with open('data/sample_data.csv', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            if row[0] == '':
                continue
            dict_.setdefault(row[1], {})
            dict_[row[1]].update({row[2]: row[3]})
    pp.pprint(dict_)
    i = 0
    for key in dict_:
        i += 1
    print(i)

