#!/usr/bin/env python

import sys, os
if len(sys.argv) < 4:
    print("%s MACRO INPUT.root OUTPUT.root" % sys.argv[0])
    sys.exit(1)
macro = sys.argv[1]
inFile = sys.argv[2]
outFile = sys.argv[3]

import ROOT
delphesPath = "Delphes"
ROOT.gSystem.AddIncludePath('-I"%s"' % delphesPath)
ROOT.gSystem.AddDynamicPath(delphesPath)
ROOT.gSystem.AddLinkedLibs('-L"%s"' % delphesPath)
ROOT.gSystem.Load("libDelphes")

ROOT.gROOT.ProcessLine(".L %s++" % macro)
ROOT.gROOT.ProcessLine('%s("%s", "%s");' % (macro.rsplit('.')[0], inFile, outFile))
