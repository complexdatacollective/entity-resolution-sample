#!/usr/bin/env python3
import sys, os, time
import argparse
import random

"""
# Random Entity Resolution

This example resolution script just assigns each pair a random value. It's useful to check that your
python system and version of server is working correctly. It includes an example of reading and writing
data from stdin/stdout using the built in sys and print tools.
"""

# Set up arguments using argparse library
parser = argparse.ArgumentParser("Random resolver")
parser.add_argument('-t', '--minimumThreshold', type=float, default=0.000, help='Ignore matches lower than this threshold')
parser.add_argument('-n', '--numMatches', type=int, default=5, help='Max number of matches')
args = parser.parse_args()

# Read in all lines into an array
lines = []

def parse_line(line):
  line_parts = line.rstrip().split(",")
  entity_type = line_parts[1].rstrip()
  return line_parts

for line in sys.stdin:
  lines.append(parse_line(line))


# Start output
for leftIndex, left in enumerate(lines):
  if leftIndex == 0:
    print("networkCanvasAlterID_1, networkCanvasAlterID_2, prob", flush=True)
    continue

  # For every unique combination:
  for rightIndex, right in enumerate(lines):
    # Don't match pairs twice
    if rightIndex <= leftIndex:
      continue

    prob = float(random.random()) # randomly assign pairs a probability

    if prob > args.minimumThreshold:
      count += 1

      if count > args.numMatches:
        exit(0)

      print(f'{left[0].rstrip()}, {right[0].rstrip()}, {prob}', flush=True)

