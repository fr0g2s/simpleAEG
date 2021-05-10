import angr, claripy
import exploitgen

class BugFinder:    
    """
        find unconstrained state with forward-SE.
        check if bp,ip register is symbolic.
        for now, no strategy for efficient explore

        Usage:
        bugFinder(arch, exploitType={}, strategy)
        - arch: target bin's arch info
        - exploitType: what exploit type to find
            -- stack 
                = return to stack (incomplete)
                = return to libc (incomplete)
                = return to code (incomplete)
            -- heap (incomplete)
                = None
        - strategy: exploring strategy
            -- None
    """

    def __init__(self, proj, func=None, exploitType={}, strategy=None):
        """
            - arch
            - exploitType
            - strategy
            - func
            - cfg
            - state
            - simgr
        """
        self.arch = proj.arch    # x86, AMD64, 
        self.exploitType = exploitType
        self.strategy = strategy
        self.func = func
        self.cfg = self.__getCFG(proj)
        self.state = self.__getState(proj, func)
        self.simgr = self.__getSimgr(proj, self.state)

    def __getCFG(self, proj):
        cfg = proj.analyses.CFGFast()
        return cfg

    def __getSimgr(self, proj, st):
        simgr = proj.factory.simulation_manager(st)
        return simgr

    def getFuncAddr(self, cfg, func_name):
        for addr, func in cfg.kb.functions.items():
            if func.name == func_name:
                return addr
        return None

    def __getState(self, proj, func):
        """
            if func given, return call_state(func). if not, return entry_state()
            state need stdin? argv?
        """
        if func:
            addr = self.getFuncAddr(self.cfg, func)
            if addr:
                state = proj.factory.call_state(addr)
                return state
        state = proj.factory.entry_state()
        return state

    def getExploitableState(self):
        """
            return [exploitable states]
            @) exploitable state constraints )
             | - symbolic ip regs           |
             | - ???                        |
             | ...                          |
        """
        simgr = self.simgr
        while len(simgr.unconstrained) == 0:
            simgr.step()

        exploitableState = []
        if len(simgr.unconstrained) > 0:
            print('[*] found %d unconstrained state' % len(simgr.unconstrained))
            for ust in simgr.unconstrained:
                if not self.__isExploitable(ust):
                    exploitableState.append({'state':ust, 'exploitable':False})   # unconstrained but unexploitable
                exploitableState.append({'state':ust, 'exploitable':True})    # unconstrained and exploitable
        if len(exploitableState) > 0:
            return exploitableState
        else:
            return False

    def __isExploitable(self, state):
        """
            check only ip register's symbolic
        """
        ip = state.ip.args[0]
        if state.solver.symbolic(ip) is True:
            return True
        return False
