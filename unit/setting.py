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
		self.st = self.p.factory.call_state(
				self.p.loader.find_symbol("main").rebased_addr,
				stdin=self._getStdin(),
				add_options=extras
				)
		self.sm = self.p.factory.simulation_manager(self.st)
		self.expst = []
		self.obj =self.p.loader.main_object

	def _getStdin(self):
		myinput_ = [claripy.BVS('myinput_%d' % i, 8) for i in range(0, mx_len, 1)]
		myinput = claripy.Concat(*myinput_)
		return myinput

	def find_unconstrained(self):
		while len(self.sm.unconstrained) == 0:
			self.sm.step()
			
		if len(self.sm.unconstrained) > 0:
			print('found %d unconstrained states' % len(self.sm.unconstrained))
			for ust in self.sm.unconstrained:
				self.expst.append(ust)
