
import os

lines = []
with open('results.csv', 'r') as fr:
    lines = fr.readlines()

scores = {}
for line in lines[1:]:
    dataset, model, src, trg, pass_1_greedy, pass_1, pass_5, verified, conversational, paper = line.strip().split(',')
    scores.setdefault(model, {'verified': verified, 'conversational': conversational, 'paper': paper})
    scores[model].setdefault(src, {})
    scores[model][src].setdefault(trg, {})
    scores[model][src][trg].setdefault('pass_1_greedy', [])
    scores[model][src][trg].setdefault('pass_1', [])
    scores[model][src][trg].setdefault('pass_5', [])
    scores[model][src][trg]['pass_1_greedy'].append(float(pass_1_greedy))
    if pass_1 == '-' or pass_5 == '-':
        continue
    scores[model][src][trg]['pass_1'].append(float(pass_1))
    scores[model][src][trg]['pass_5'].append(float(pass_5))

average_scores = {}
for model in scores:
    average_scores.setdefault(model, {})
    for src in scores[model]:
        if src in ['verified', 'conversational', 'paper']:
            average_scores[model][src] = scores[model][src]
            continue
        average_scores[model].setdefault(src, {})
        for trg in scores[model][src]:
            average_scores[model][src].setdefault(trg, {})
            for metric in scores[model][src][trg]:
                if len(scores[model][src][trg][metric]) == 0:
                    average_scores[model][src][trg][metric] = '-'
                    continue
                average_scores[model][src][trg][metric] = round(sum(scores[model][src][trg][metric]) / len(scores[model][src][trg][metric]), 2)

for model in average_scores:
    for src in average_scores[model]:
        if src in ['verified', 'conversational', 'paper']:
            continue
        for trg in average_scores[model][src]:
            print(f"All Datasets,{model},{src},{trg},{average_scores[model][src][trg]['pass_1_greedy']},{average_scores[model][src][trg]['pass_1']},{average_scores[model][src][trg]['pass_5']},{average_scores[model]['verified']},{average_scores[model]['conversational']},{average_scores[model]['paper']}")

