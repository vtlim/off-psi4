#!/usr/bin/env python
#
# Adpated from OpenEye
#  - Source: https://docs.eyesopen.com/toolkits/python/_downloads/catmols.py
#  - Edited to remove the OEAddMols command to keep molecules separate
#  - Edited to skip molecules with specified titles from the parent file (first file listed)
#
# Examples:
#  - python catMols2.py -i diverse-200-Div1.mol2 diverse-200-Div4.mol2 -o 41.mol2
#  - python catMols2.py -i diverse-200.sdf diverse-200-Div4-selected.mol2 -list exclude.txt -o new.sdf
#
# By: Victoria T. Lim
#
#############################################################################
# Copyright (C) 2008-2015 OpenEye Scientific Software, Inc.
#############################################################################
# This program concatenates molecules into one file.
# It can be useful for generating ROCS queries or reattach ligands to an
# protein structure
#############################################################################
import sys
from openeye.oechem import *

def CatMols(infnames, outfname,nameset):
    ofs = oemolostream()
    if not ofs.open(outfname):
        OEThrow.Fatal("Unable to open %s for writing" % outfname)

    for i, fname in enumerate(infnames):
        print(fname, i)
        ifs = oemolistream()
        if ifs.open(fname):
            for imol in ifs.GetOEGraphMols():
                if imol.GetTitle() in nameset and i==0:
                    continue
                else:
                    OEWriteMolecule(ofs, imol)
        else:
            OEThrow.Fatal("Unable to open %s for reading" % fname)




Interface = """
!BRIEF -i <infile1> [<infile2>...] -o <outfile>
!PARAMETER -i
  !ALIAS -in
  !TYPE string
  !LIST true
  !REQUIRED true
  !BRIEF input file name(s)
!END
!PARAMETER -o
  !ALIAS -out
  !TYPE string
  !REQUIRED true
  !BRIEF output file name
!END
!PARAMETER -title
  !ALIAS -t
  !TYPE string
  !LIST true
  !BRIEF Single or space-separated list of titles to exclude from parent file
!END
!PARAMETER -list
  !ALIAS -l
  !TYPE string
  !BRIEF List file of mol titles to exclude from parent file
!END
"""


def main(argv=[__name__]):
    itf = OEInterface(Interface, argv)

    # collect names
    nameset = set()
    if itf.HasString("-list"):
        try:
            lfs = open(itf.GetString("-list"))
        except IOError:
            OEThrow.Fatal("Unable to open %s for reading" % itf.GetString("-list"))
        for name in lfs.readlines():
            name = name.strip()
            nameset.add(name)
    elif itf.HasString("-title"):
        for t in itf.GetStringList("-title"):
            nameset.add(t)

    CatMols(itf.GetStringList("-i"), itf.GetString("-o"), nameset)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
