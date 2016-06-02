import json
from sklearn.datasets import fetch_20newsgroups


'''
    store comp.graphics jsonl file in target folder
'''


categories = ['alt.atheism', 'soc.religion.christian', 'comp.graphics', 'sci.med']
twenty_train = fetch_20newsgroups(subset='train',
                                  categories=categories, shuffle=True, random_state=42)
twenty_test = fetch_20newsgroups(subset='test',
                                 categories=categories, shuffle=True, random_state=42)


target_content = ''
for item in twenty_train.target:
    if twenty_train.target_names[item] == 'comp.graphics':
        target_content += twenty_train.data[item]

with open('test/target.jsonl', 'w') as tfile:
    json.dump({'name':'target', 'content': target_content}, tfile)

with open('test/candidate.jsonl', 'w') as cfile:
    for item in twenty_test.target:
        json.dump({'name': twenty_test.target_names[item],
                   'content': twenty_test.data[item]
                  }, cfile)
        cfile.write('\n')
