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


def robinhood(username, given_to_others, dict_scores, all_usernames):
    distribution_list = dict()

    for k, v in given_to_others.items():
        if k == username:
            # self-awarded credit
            # redistribute that credit out to the people who gave you credit
            # reference: https://stackoverflow.com/questions/21507375/how-does-pageranking-algorithm-deal-with-webpage-without-outbound-links
            distribution_list[username] = list()
            for k2, v2 in dict_scores.items():
                if username in v2 and k2 != username:
                    distribution_list[username].append(k2)

            # if they are the only ones who gave credit to themselves, redistribute it to everyone else in the entire network
            if len(distribution_list[username]) == 0:
                distribution_list[username].extend([item for item in all_usernames if item != username])

    for k, v in distribution_list.items():
        try:
            ration_per_user = given_to_others[k] / float(len(v))
        except ZeroDivisionError:
            ration_per_user = 0
        # print("%f total, %f per person" % (given_to_others[k], ration_per_user))
        for other_username in v:
            if other_username in given_to_others:
                given_to_others[other_username] += ration_per_user
            else:
                given_to_others[other_username] = ration_per_user

    return dict(given_to_others)


def to_weighted_edges(dict_scores, all_usernames):
    weighted_edges = []
    for to_user in dict_scores:
        username = to_user
        given_to_others = dict_scores[to_user]
        given_to_others = normalize_dict_values(given_to_others)
        given_to_others = robinhood(username, given_to_others, dict_scores, all_usernames)
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
    return result
