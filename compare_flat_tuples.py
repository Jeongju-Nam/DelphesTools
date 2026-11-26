#!/usr/bin/env python3

import sys

import ROOT

if len(sys.argv) < 3:
    print("%s BEFORE.root AFTER.root" % sys.argv[0])
    sys.exit(1)

f_before = ROOT.TFile(sys.argv[1])
f_after = ROOT.TFile(sys.argv[2])
t_before = f_before.Get("Events")
t_after = f_after.Get("Events")

names_before = {b.GetName() for b in t_before.GetListOfBranches()}
names_after = {b.GetName() for b in t_after.GetListOfBranches()}
if names_before - names_after:
    print("Only before:", sorted(names_before - names_after))
if names_after - names_before:
    print("Only after:", sorted(names_after - names_before))
common = sorted(names_before & names_after)

# An array branch such as Jet_pt has a count leaf (nJet) that holds its length in each event
length_of = {}
for name in common:
    count = t_before.GetLeaf(name).GetLeafCount()
    length_of[name] = count.GetName() if count else None

different = set()
n_events = t_before.GetEntries()
if t_after.GetEntries() != n_events:
    print("Different numbers of events:", n_events, t_after.GetEntries())

for i in range(n_events):
    t_before.GetEntry(i)
    t_after.GetEntry(i)
    for name in common:
        if name in different:
            continue
        value_before = getattr(t_before, name)
        value_after = getattr(t_after, name)
        if length_of[name]:
            n_before = getattr(t_before, length_of[name])
            n_after = getattr(t_after, length_of[name])
            same = n_before == n_after and all(
                value_before[k] == value_after[k] for k in range(n_before)
            )
        else:
            same = value_before == value_after
        if not same:
            different.add(name)

print("Branches compared:", len(common))
print("Different branches:", sorted(different) if different else "none")
