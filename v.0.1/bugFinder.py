import angr, claripy
import exploitGen

class bugFinder:    
    """
        find unconstrained state with forward-SE.
        check if bp,ip register is symbolic.
        for now, no strategy for efficient explore

        Usage:
        bugFinder(arch, exploitType={}, strategy)
        - arch: target bin's arch info
        - exploitType: what exploit type to find
            -- stack 
                = return to stack
                = return to libc
                = return to code
            -- heap
                = None
        - strategy: exploring strategy.
            -- None
    """

    def __init__(self, arch, exploitType={},strategy=None):
        self.arch = arch    # x86, AMD64, 
        self.exploitType = exploitType
        self.strategy = strategy

    def getExploitableState(self, simgr):
        """
            return unconstrained(exploitable) state
        """
        while len(simgr.unconstrained) == 0:
            simgr.step()

        exploitableState = []
        if len(simgr.unconstrained) > 0:
            print('[*] found %d unconstrained state' % len(simgr.unconstrained))
            for ust in simgr.unconstrained:
                if not self.isExploitable(ust):
                    continue
                exploitableState.append(ust)
        if len(exploitableState) > 0:
            return exploitableState
        else:
            return False

    def isExploitable(self, state):
        """
            check only ip register's controllability
        """
        ip = state.pc.args[0]
        if state.solver.symbolic(ip) is True:
            return True
        return False
