#!/usr/bin/python3

import bugfinder
import exploitgen
import verifier
import angr
import sys
import os
import code

USAGE = """
    $ ./main.py `target bin`
"""

def getMitigate(p):
    """
        [ TEST ]
        angr.loader.main_object 
    """
    mitigate = {}
    mainobj = p.loader.main_object
    mitigate['NX'] = mainobj.execstack
    mitigate['PIE'] = mainobj.pic
    mitigate['RELRO'] = str(mainobj.relro)  # Relro.NONE | Relro.PARTIAL | Relro.FULL

    return mitigate

def main(target):
    proj = angr.Project(target, load_options={"auto_load_libs":False})
    arch = proj.arch
    finder = bugfinder.BugFinder(proj, func='main')
    print("""
        - arch: {0}
        - exploitType: {1}
        - strategy: {2}
        - func: {3}
        - cfg: {4}
        - state:  {5}
        - simgr: {6}
    """.format(finder.arch, finder.exploitType, finder.strategy, finder.func, finder.cfg, finder.state, finder.simgr))
    expst_list = finder.getExploitableState()
    cnt = 1
    for expst in expst_list:
        print('[FOUND: {0}] ip regs symbolic: {1}'.format(cnt, expst['state'].solver.symbolic(expst['state'].ip.args[0])))
        print(
        """
            st: {0}
            exploitable: {1}
        """.format(expst['state'], expst['exploitable']))
        if expst['exploitable'] is False:
            continue
        print('= what data inputed? =')
        print('len: ', len(expst.posix.dumps(0)))
        print(expst.posix.dumps(0))
        cnt += 1
    #generator = exploitgen.ExploitGen(arch)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(USAGE)
        sys.exit(0)
    main(sys.argv[1])

