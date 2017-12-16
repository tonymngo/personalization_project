import json

import pprint

pp = pprint.PrettyPrinter(indent=4, width=180)

if __name__ == '__main__':
    with open('data/meta_Grocery_and_Gourmet_Food.json', 'r') as file:
        data = file.read()

    # for item in data:
    #     pp.pprint(item)

    data = json.dumps(data)

    # with open('data/edit.json', 'w') as file:
    #     file.write(data)

    json_dict = json.loads(data)

    for i,j in json_dict.items():
        pp.pprint((i,j))



        # for line in data:
        #     line = json.dumps(line)
        #     pp.pprint(line)
