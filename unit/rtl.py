import setting
import angr, claripy
import code

base = setting.Base('./t1', mx_len=0x30)
base.find_unconstrained()
code.interact(local=locals())

