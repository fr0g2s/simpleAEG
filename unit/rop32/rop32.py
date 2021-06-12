import setting
import code
import weapon
import sys
from pwn import *

class Possible:
	OVERWRITE = False
	LEAK = False
	EXEC = False

class MyWeapon:
	def __init__(self, target):
		self.e = ELF(target)
		self.possible = Possible()
		self.overwrite_funcs = {}
		self.leak_funcs = {}
		self.exec_funcs = {}	# not use

		self._set_gadgets()

	def _set_gadgets(self):
		weapon_funcs = weapon.functions()
		
		for sym,addr in self.e.plt.items():
			if sym in weapon_funcs.mem_write:
				self.overwrite_funcs[sym] = addr
				self.possible.OVERWRITE = True
			if sym in weapon_funcs.mem_read:
				self.leak_funcs[sym] = addr
				self.possible.LEAK = True
			if sym in weapon_funcs.execute:
				self.exec_funcs[sym] = addr
				self.possible.EXEC = True
		
	def check_exploitable(self):
		# satisfy this condition, we can make exploit payload (for now) 
		if self.possible.OVERWRITE and self.possible.LEAK:
			return True
		else:
			return False

def get_rop_payload(my_weapon, recv_len):	# 몇바이트 leak을 해야하나? -> st.posix.dumps(1) 이용
	payload = ''
	leak_func = next(iter(my_weapon.leak_funcs.values()))
	overwrite_func = next(iter(my_weapon.overwrite_funcs.values()))

	return payload

def get_usable_len(st, mx_len):
	pc_flag = b'aaaa'
	st.solver.add(st.regs.pc == pc_flag)
	pc_idx = st.posix.dumps(0).index(pc_flag)
	usable_len = mx_len - pc_idx
	code.interact(local=locals())

def main():
	b = setting.Base('./t1', mx_len=0x50)
	my_weapon = MyWeapon(b.p.filename)
	if my_weapon.check_exploitable() is not True:
		print("we can't make it")
		print('LEAKABLE: ', my_weapon.possible.LEAK)
		print('OVERWRITE: ', my_weapon.possible.OVERWRITE)
		print('EXEC: ', my_weapon.possible.EXEC)
		sys.exit(0)
	b.find_unconstrained()
	print('found %d unconstrained states' % len(b.expst))

	ust = b.expst[0]
	send_len = len(ust.posix.dumps(0))
	usabel_len = get_usable_len(ust, 0x50)	# ret ~ last byte
	recv_len = len(ust.posix.dumps(1))	# for leak.
	payload = get_rop_payload(my_weapon, recv_len)
	
	if len(payload) > usable_len:
		print("we can't make it")
	else:
		with open('exploit', 'wb') as f:
			f.write(payload)
		print("Done")

if __name__ == "__main__":
	main()
