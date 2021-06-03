import angr, claripy
import sys
import code
from angr import sim_options as so

class Base:
	"""
		p: angr.Project
		st: call_state('main')
		sm: simulation_manager
		expst: exploitable(unconstrained) state
		obj: proj.loader.main_object
		stdin_data: stdin data via claripy.BVS
	"""

	def __init__(self, target=None, mx_len=0x30):
		default_target = './t1'
		if target is None:
			self.target = default_target
		else:
			self.target = target
		
		load_options = {"auto_load_libs":True}	
		self.p = angr.Project(self.target, load_options=load_options)
		extras = {so.REVERSE_MEMORY_NAME_MAP}
		self.stdin_data = self._getStdin(mx_len)
		self.st = self.p.factory.call_state(
				self.p.loader.find_symbol("main").rebased_addr,
				stdin=self.stdin_data,
				add_options=extras
				)
		self.st.solver.register_variable(self.stdin_data,('myinput', 'stdin', mx_len))
		self.sm = self.p.factory.simulation_manager(self.st)
		self.expst = []
		self.obj =self.p.loader.main_object

	def _getStdin(self, mx_len):
		myinput_ = [claripy.BVS('myinput_%d' % i, 8) for i in range(0, mx_len, 1)]
		myinput = claripy.Concat(*myinput_)
		return myinput

	def find_unconstrained(self):
		while len(self.sm.unconstrained) == 0:
			self.sm.step()
			
		if len(self.sm.unconstrained) > 0:
			for ust in self.sm.unconstrained:
				self.expst.append(ust)
