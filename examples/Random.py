#!/usr/bin/env python3
import sys, os, time
import argparse
import random

parser = argparse.ArgumentParser("Random resolver")
parser.add_argument('-t', '--minimumThreshold', type=float, default=0.000, help='Ignore matches lower than this threshold')
parser.add_argument('-n', '--numMatches', type=int, default=5, help='Max number of matches')
args = parser.parse_args()

lines = []

def parse_line(line):
  line_parts = line.rstrip().split(",")
  entity_type = line_parts[1].rstrip()
  return line_parts

for line in sys.stdin:
  lines.append(parse_line(line))

count = 0

for leftIndex, left in enumerate(lines):
  if leftIndex == 0:
    print("networkCanvasAlterID_1, networkCanvasAlterID_2, prob, count", flush=True)
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

      print(f'{left[0].rstrip()}, {right[0].rstrip()}, {prob}, {count}', flush=True)
      # add an artificial delay
      # time.sleep(1)

