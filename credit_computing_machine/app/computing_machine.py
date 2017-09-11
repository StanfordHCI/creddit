#!/usr/bin/env python

import networkx as nx
import json
from collections import Counter
import csv

class PrettyFloat(float):
    def __repr__(self):
        return '%.2f' % self

def pretty_floats(obj):
    if isinstance(obj, float):
        return PrettyFloat(obj)
    elif isinstance(obj, dict):
        return dict((k, pretty_floats(v)) for k, v in obj.items())
    elif isinstance(obj, (list, tuple)):
        return map(pretty_floats, obj)
    return obj

def normalize_dict_values(d):
  sum_vals = sum(d.values())
  output = {}
  for k,v in d.items():
    output[k] = float(v) / sum_vals
  return output

def robinhood(d, all_usernames):
  threshold = 0.15
  output = Counter()
  for k,v in d.items():
    if v > threshold:
      excess = v - threshold
      output[k] += threshold
      ration_per_user = excess / float(len(all_usernames))
      for other_username in all_usernames:
        output[other_username] += ration_per_user
    else:
      output[k] += v
  return dict(output)

overrides = {}

def to_weighted_edges(csv_lines, all_usernames):
  weighted_edges = []
  for line in csv_lines:
    username = line['Choose your Slack username']
    given_to_others = {}
    if username in overrides:
      given_to_others = overrides[username]
    for target_user in all_usernames:
      if username in overrides:
        break
      if target_user == username:
        continue
      if line[target_user] == '':
        continue
      value_given = float(line[target_user])
      if not 0 < value_given < float('inf'):
        continue
      given_to_others[target_user] = value_given
    if len(given_to_others) == 0:
      continue
    import pdb
    pdb.set_trace()
    #print(111111111111111)
    #print(given_to_others)
    given_to_others = normalize_dict_values(given_to_others)
    given_to_others = robinhood(given_to_others, all_usernames)
    #print(22222222222)
    print(target_user)
    #print(value_given)
    for target_user,value_given in given_to_others.items():
      weighted_edges.append((username, target_user, value_given))
    print(weighted_edges)
  return weighted_edges

csv_lines = csv.DictReader(open('crowdcred.csv'))
all_usernames = [x for x in csv_lines.fieldnames if x not in ['Timestamp', 'Choose your Slack username', 'Please enter your email id, using which you signed up for Slack', 'Please enter your email id that you want should go in the paper', 'Please enter your Github id', 'Please enter your current affiliation that you want should go in the paper', 'What has been your prime contribution?', 'How many weeks have you been mostly active?', 'What was your prime metric of evaluation or score distribution?']]
print(all_usernames)
weighted_edges = to_weighted_edges(csv_lines, all_usernames)

who_voted_for_each_user = {}
for giver,receiver,value_given in weighted_edges:
  if receiver not in who_voted_for_each_user:
    who_voted_for_each_user[receiver] = {}
  who_voted_for_each_user[receiver][giver] = value_given

G = nx.DiGraph()
G.add_nodes_from(all_usernames)
G.add_weighted_edges_from(weighted_edges)

pagerank_results = nx.algorithms.link_analysis.pagerank_alg.pagerank(G, alpha=0.85, max_iter=10000)
score_and_username = [(score,username) for username,score in pagerank_results.items()]
for score,username in sorted(score_and_username, reverse=True):
  voters = {}
  if username in who_voted_for_each_user:
    voters = who_voted_for_each_user[username]
  print username.encode('utf-8'), 'score=' + str(score) #, 'voters=' + str(pretty_floats(sorted(voters.items())))
  print ''