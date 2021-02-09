#!/usr/bin/env python3
import pandas as pd
import numpy as np
import sys, os, time
import argparse
import random
import recordlinkage


name_field = '6be95f85-c2d9-4daf-9de1-3939418af888'
surname_field = '0ff25001-a2b8-46de-82a9-53143aa00d10'
person_entity_type = '4aebf73e-95e3-4fd1-95e7-237dcc4a4466'

parser = argparse.ArgumentParser("Entity resolver resolver")
parser.add_argument('-t', '--minimumThreshold', type=float, default=0.000, help='Ignore matches lower than this threshold')
args = parser.parse_args()

# script_path = os.path.dirname(__file__)
# csv_path = os.path.join(script_path, "EntityResolution_attributeList.csv")
# df  =  pd.read_csv(csv_path, delimiter=',',index_col='networkCanvasAlterID')

df = pd.read_csv(sys.stdin, delimiter=',')

# Remove duplicate ids
df.drop_duplicates('networkCanvasAlterID', keep = False, inplace = True)
df.set_index("networkCanvasAlterID", inplace = True)
person_nodes = df.loc[df['networkCanvasNodeType'] == person_entity_type];

# time.sleep(10)


# Merge dataframe to itself to get pairwise comparisons
indexer = recordlinkage.Index()
indexer.full()
index_list = indexer.index(person_nodes)
comp_pairs = recordlinkage.Compare()
comp_pairs.string(name_field, name_field, method='jarowinkler',label='fnJwDist')
comp_pairs.string(surname_field, surname_field, method='jarowinkler',label='lnJwDist')
comp_pairs.string(name_field, name_field, method='levenshtein',label='fnLevenDist')
comp_pairs.string(surname_field, surname_field, method='levenshtein',label='lnLevenDist')
pairwise = comp_pairs.compute(index_list, person_nodes)

erAlgorithm = "simple"
algorithmError = "Please specify an appropriate algorithm"
if erAlgorithm == "simple": # Use simple mean of all string distances
    pairwise["prob"] = pairwise.mean(axis=1)
elif erAlgorithm == "logReg": # Use logistic regression
    features = ['fnJwDist','fnLevenDist','lnJwDist','lnLevenDist']
    from joblib import dump, load
    from sklearn.linear_model import LogisticRegression
    logRegModel = load('pugLogRegression.joblib')
    pairwise['prob'] = logRegModel.predict_proba(pairwise[features])[:,1]
elif erAlgorithm == "decisionTree":     # Use degression tree
    features = ['fnJwDist','fnLevenDist','lnJwDist','lnLevenDist']
    from joblib import dump, load
    from sklearn.tree import DecisionTreeRegressor
    treeModel = load('pugDecisionTree.joblib')
    pairwise['prob'] = treeModel.predict(pairwise[features])
else:
    print(algorithmError)

# Output edgelist w/ probability
foo = pairwise[['prob']].to_csv(index=True)

# spoof slow streamed response
for index, line in enumerate(foo.splitlines()):
    # time.sleep(0.05)
    if index == 0:
        print(line, flush=True)
        continue

    line_parts = line.split(",")
    prob = float(line_parts[2])
    if (prob > args.minimumThreshold):
        print(line, flush=True)
