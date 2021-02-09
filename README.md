# Entity Resolution Sample Scripts

This repository provides some sample scripts and a sample protocol for use with the Entity Resolution feature in Network Canvas Server.

# How entity resolution works

Entity resolution allows you to find pairs of nodes (and egos) across different sessions that represent the same person, place or object.
You can export a single network including these merged nodes, and their resolved properties. This is facilitated by sending a list
of nodes to your script (typically python), which then returns a list of pairs with scores of the probability of matching.

### Egos
Egos are "cast" (converted) into a type of node from the network during the resolution process. Attributes are matched
according to their labels. e.g. if ego has the attribute 'name', and the person node type has the attribute 'name', when the ego is cast as a person node it will copy this value accross.

# Writing an entity

1. A `CSV` formatted list of nodes (and attributes) are sent to your entity resolution script via `stdin`.
2. The script can process these nodes any way you choose.
3. The script should write to `stdout` with a list of node pairs and their probability score.

## stdin example

An example of data that will be sent to your script.

```csv
id,type,name,age
1,4aebf73e-95e3-4fd1-95e7-237dcc4a4466,Abigail,40
2,4aebf73e-95e3-4fd1-95e7-237dcc4a4466,Bianca,41
3,4aebf73e-95e3-4fd1-95e7-237dcc4a4466,Charlotte,37
4,4aebf73e-95e3-4fd1-95e7-237dcc4a4466,David,23
5,4aebf73e-95e3-4fd1-95e7-237dcc4a4466,Eugene,56
```

Example code to read in this data:

```python
lines = []

for line in sys.stdin:
  lines.append(line)

# process data (`lines`) here

```

Or using the `pandas` library:

```python
import pandas

data_frame = pandas.read_csv(sys.stdin, delimiter=',')

# process data frame here
```

## stdout example

An example of data that your script should output. The field headings
are mandatory and fixed.

```csv
networkCanvasAlterID_1, networkCanvasAlterID_2, prob
1,2,0.500
2,3,0.900
3,4,0.995
```

Example code to output from script:

```python
print("networkCanvasAlterID_1, networkCanvasAlterID_2, prob", flush=True)
# `flush=True` stops output being buffered until the program completes and prints it immediately.
# Network Canvas Server can start to present results to the user as soon as they
# start coming in, the script need not have completed.

for line in results:
    print(f'{line['id1']}, {line['id2']}, {line['prob']}', flush=True)
```

# Example scripts

### EntityResolution.py

This script finds matches by their Levenshtein, Jaro-Winkler distances,
and is a potential real-world example.

### Random.py

This script assigns pairs with a random probabiltiy, it's useful for
testing and perhaps as a starting point for your own scripts.

# Limitations

Egos are not specifically included in the resolved network, but
if they are matched with nodes in a network, their attributes
can be used in resolution.