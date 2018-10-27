
# local testing vs. travis testing
try:
    from quanformer.confs2psi import *
except ModuleNotFoundError:
    import sys
    sys.path.insert(0, '/beegfs/DATA/mobley/limvt/openforcefield/pipeline/github/quanformer')
    from confs2psi import *

# define location of input files for testing
import os
mydir = os.path.dirname(os.path.abspath(__file__))

# -----------------------

import pytest
from helper import *


def test_make_hessian():
    mol = read_mol(os.path.join(mydir,'data_tests','methane_c2p.sdf'))
    test_string = make_psi_input(mol,mol.GetTitle(),'mp2','aug-cc-pVTZ','hess')
    assert "H, wfn = hessian('mp2', return_wfn=True)" in test_string
    assert "wfn.hessian().print_out()" in test_string

def test_make_frozen():
    mol = read_mol(os.path.join(mydir,'data_tests','freeze.sdf'))
    test_string = make_psi_input(mol,mol.GetTitle(),'mp2','aug-cc-pVTZ')
    assert "4 xyz" in test_string
    assert "1 xyz" in test_string
    assert "3 xyz" in test_string
    assert "12 xyz" in test_string

def test_make_dfmp2_dunning():
    mol = read_mol(os.path.join(mydir,'data_tests','methane_c2p.sdf'))
    test_string = make_psi_input(mol,mol.GetTitle(),'mp2','aug-cc-pVTZ')
    assert "df_basis_mp2" not in test_string

def test_make_dfmp2_qzvpd():
    mol = read_mol(os.path.join(mydir,'data_tests','methane_c2p.sdf'))
    test_string = make_psi_input(mol,mol.GetTitle(),'mp2','def2-qzvpd')
    assert "df_basis_mp2" not in test_string
    return

def test_make_dfmp2_svpp():
    mol = read_mol(os.path.join(mydir,'data_tests','methane_c2p.sdf'))
    test_string = make_psi_input(mol,mol.GetTitle(),'mp2','def2-sv(p)')
    assert "def2-sv_p_-ri" in test_string
    return

def test_confs2psi():
    return

# test manually without pytest
if 0:
    test_make_hessian()
