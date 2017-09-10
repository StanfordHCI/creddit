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
    for k, v in d.items():
        try:
            output[k] = float(v) / sum_vals
        except ZeroDivisionError:
            output[k] = 0
    return output


def robinhood(d, all_usernames):
    threshold = 0.15
    output = Counter()
    for k, v in d.items():
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


def to_weighted_edges(dict_scores, all_usernames):
    weighted_edges = []
    for to_user in dict_scores:
        username = to_user
        given_to_others = dict_scores[to_user]
        given_to_others = normalize_dict_values(given_to_others)
        given_to_others = robinhood(given_to_others, all_usernames)
        for target_user, value_given in given_to_others.items():
            weighted_edges.append((username, target_user, value_given))
    return weighted_edges


def compute_scores(dict_scores):
    all_usernames = []
    result = {}
    for to_user in dict_scores:
        all_usernames.append(to_user)
    weighted_edges = to_weighted_edges(dict_scores, all_usernames)
    who_voted_for_each_user = {}
    for giver, receiver, value_given in weighted_edges:
        if receiver not in who_voted_for_each_user:
            who_voted_for_each_user[receiver] = {}
        who_voted_for_each_user[receiver][giver] = value_given

    G = nx.DiGraph()
    G.add_nodes_from(all_usernames)
    G.add_weighted_edges_from(weighted_edges)

    pagerank_results = nx.algorithms.link_analysis.pagerank_alg.pagerank(G, alpha=0.85, max_iter=10000)
    score_and_username = [(score, username) for username, score in pagerank_results.items()]
    for score, username in sorted(score_and_username, reverse=True):
        voters = {}
        if username in who_voted_for_each_user:
            voters = who_voted_for_each_user[username]
        # print(str(username.encode('utf-8')) + 'score=' + str(
        #     score))  # , 'voters=' + str(pretty_floats(sorted(voters.items()))))
        # print(' ')
        result[username] = score
    return  result