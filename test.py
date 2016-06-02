import json
from sklearn.datasets import fetch_20newsgroups


'''

    the below is meant to represent the resume comparison scenario

    here we create a target by writing the comp.graphics
    newsgroup data from the train set to one line in the target jsonl file
    we will use this data to 'train' the model

    we then write newsgroup data from all categories to the candidate jsonl
    file for comparison to the target data

    if this approach works we would expect documents labeled comp.graphics
    in the candidate data to have lower similarity scores

'''


categories = ['alt.atheism', 'soc.religion.christian', 'comp.graphics', 'sci.med']
twenty_train = fetch_20newsgroups(subset='train',
                                  categories=categories, shuffle=True, random_state=42)
twenty_test = fetch_20newsgroups(subset='test',
                                 categories=categories, shuffle=True, random_state=42)


target_content = ''
for i in range(len(twenty_train.data)):
    if twenty_train.target_names[twenty_train.target[i]] == 'comp.graphics':
        target_content += twenty_train.data[i]

with open('test/target.jsonl', 'w') as tfile:
    json.dump({'name':'target', 'content': target_content}, tfile)

with open('test/candidate.jsonl', 'w') as cfile:
    for i in range(len(twenty_test.data)):
        json.dump({'name': twenty_test.target_names[twenty_test.target[i]],
                   'content': twenty_test.data[i]
                  }, cfile)
        cfile.write('\n')
