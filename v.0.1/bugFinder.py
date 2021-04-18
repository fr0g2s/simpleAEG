import angr, claripy

# frame
class bugFinder:    
    def __init__(self, bin_name, isStdin=None, max_len=0, isArgs=None, args_cnt):
        self.isStripped = False
        self.main_addr = None
        self.isArgs = isArgs
        self.args = [bin_name]
        self.args_cnt = args_cnt
        self.isStdin = isStdin
        self.len = max_len  # all input data's length have max_len (heuristic)
        self.stdin_data = []

    def getFuncAddr(self, cfg, func_name):
        for addr, func in cfg.kb.functions.items():
            if func_name == func.name:
                return addr
        return None
    
    def setProj(self):
        self.proj = angr.Project(self.bin_name, load_options={'auto_load_libs':False})
        cfg = self.proj.analyses.CFG(fail_fast=True)
        self.main_addr = self.getFuncAddr(cfg, 'main')        
        if self.main_addr is None:
            self.isStripped = True    
        self.setState()

    def setState(self):
        if self.isStdin is True:
            self.setStdin()
        if self.isArgs is True:
            self.setArgs()

        if isStripped is True:  # if stripped binary, use entry_state()
            self.state = self.proj.factory.entry_state(args=self.args, stdin=self.data)
        else:   # if we can use symbol info, use call_state(main)
            self.state = self.proj.factory.call_state(self.main_addr, args=self.args, stdin=angr.SimFile('/dev/stdin',self.stdin_data))

        self.setConstraints()

    def setStdin(self):
        self.stdin_data = claripy.BVS('stdin_data', 8 * self.len)
    
    def setArgs(self):
        for i in range(0, self.args_cnt, 1):
            self.args.append(claripy.BVS('args_%d' i, 8*self.len))

    def setConstraints(self):   # not null ?
        pass

