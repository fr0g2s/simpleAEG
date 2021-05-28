import angr, claripy
import sys
import code
from angr import sim_options as so

class Base:
	def __init__(self, target=None, mx_len=0x30):
		default_target = './t1'
		if target is None:
			self.target = self.default_target
		else:
			self.target = target

		self.p = angr.Project(self.target)
		extras = {so.REVERSE_MEMORY_NAME_MAP}
		myinput_ = [claripy.BVS('myinput_%d' % i, 8) for i in range(0, mx_len, 1)]
		self.st = self.p.factory.call_state(
				self.p.loader.find_symbol("main").rebased_addr,
				add_options=extras
				)
		self.sm = self.p.factory.simulation_manager(self.st)

	def show_sym_buff(st, p):
		sym_addrs = []
		print('st, sym_addrs, p')
		code.interact(local=locals())

		p = angr.Project(target)
		extras = {so.REVERSE_MEMORY_NAME_MAP}
		myinput_ = [claripy.BVS("myinput_%d" % i, 8) for i in range(0,0x30,1)]
		myinput = claripy.Concat(*myinput_)
		st = p.factory.call_state(p.loader.find_symbol('main').rebased_addr, add_options=extras, stdin=myinput)
		st.solver.register_variable(myinput, ('myinput', 0x200))
		sm = p.factory.simulation_manager(st)

		while len(sm.unconstrained) == 0:
			sm.step()
		
		if len(sm.unconstrained) > 0:
			print('found %d unconstrained states' % len(sm.unconstrained))
			for ust in sm.unconstrained:
				show_sym_buff(ust, p)

