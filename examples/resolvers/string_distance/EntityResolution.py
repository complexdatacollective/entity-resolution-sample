#!/usr/bin/env python3
import pandas as pd
import numpy as np
import sys
import argparse
import random
import recordlinkage

"""
# String Distance Entity Resolution

This example resolution script assigns a score according to word distance.

It includes an example of reading data from stdin using pandas.
"""

name_field = '722f07ae-c166-405a-a47b-7b4f85e7e411' # `/examples/protocols/SimpleEntityResolutionProtocol.netcanvas` name field
erAlgorithm = 'simple' # Algorithm to compare distances

# Set up arguments using argparse library
parser = argparse.ArgumentParser("Entity resolver resolver")
parser.add_argument('-t', '--minimumThreshold', type=float, default=0.000, help='Ignore matches lower than this threshold')
args = parser.parse_args()

# Read file into pandas from sdin
df = pd.read_csv(sys.stdin, delimiter=',')

# Remove duplicate ids
df.drop_duplicates('networkCanvasAlterID', keep = False, inplace = True)
df.set_index("networkCanvasAlterID", inplace = True)
person_nodes = df.loc[df['networkCanvasNodeType'] == person_entity_type];

# Merge dataframe to itself to get pairwise comparisons
indexer = recordlinkage.Index()
indexer.full()
index_list = indexer.index(person_nodes)
comp_pairs = recordlinkage.Compare()
comp_pairs.string(name_field, name_field, method='jarowinkler',label='fnJwDist')
comp_pairs.string(name_field, name_field, method='levenshtein',label='fnLevenDist')
pairwise = comp_pairs.compute(index_list, person_nodes)

algorithmError = "Please specify an appropriate algorithm"
if erAlgorithm == "simple": # Use simple mean of all string distances
    pairwise["prob"] = pairwise.mean(axis=1)
elif erAlgorithm == "logReg": # Use logistic regression
    features = ['fnJwDist','fnLevenDist']
    from joblib import dump, load
    from sklearn.linear_model import LogisticRegression
    logRegModel = load('pugLogRegression.joblib')
    pairwise['prob'] = logRegModel.predict_proba(pairwise[features])[:,1]
elif erAlgorithm == "decisionTree":     # Use degression tree
    features = ['fnJwDist','fnLevenDist']
    from joblib import dump, load
    from sklearn.tree import DecisionTreeRegressor
    treeModel = load('pugDecisionTree.joblib')
    pairwise['prob'] = treeModel.predict(pairwise[features])
else:
    print(algorithmError)

# Get results as csv format
result = pairwise[['prob']].to_csv(index=True)

# Output results to stdout
for index, line in enumerate(result.splitlines()):
    # CSV headers
    if index == 0:
        print(line, flush=True) # flush=True output immediately, not at end of script
        continue

    # For each pair check that it matches the minimum threshold
    line_parts = line.split(",")
    prob = float(line_parts[2])
    if (prob > args.minimumThreshold):
        print(line, flush=True)
