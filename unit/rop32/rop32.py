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
		self.exec_funcs = {}
		self.

		self.set_gadgets()

	def _set_gadgets(self):
		weapon_funcs = weapon.functions()

		for sym,addr in e.plt.items():
			if sym in weapon_funcs.mem_write:
				overwrite_funcs[sym] = addr
				OVERWRITE = True
			if sym in weapon_funcs.mem_read:
				leak_funcs[sym] = addr
				LEAK = True
			if sym in weapon_funcs.execute:
				exec_funcs[sym] = addr
				EXEC = True
		
	def check_exploitable(self):
		# satisfy this condition, we can make exploit payload (for now) 
		if self.possible.OVERWRITE and self.possible.LEAK and self.possible.EXEC:
			return True
		else:
			return False

def get_rop_payload(my_gadget):	# 몇바이트 leak을 해야하나? -> st.posix.dumps(1) 이용
	payload = ''
	return payload

def main():
	b = setting.Base('./t1', mx_len=0x50)
	my_gadget = MyGadgets(b.p.filename)
	if my_gadget.check_exploitable() is not True:
		print("we can't make it")
		sys.exit(0)
	b.find_unconstrained()
	print('found %d unconstrained states' % len(b.expst))

	ust = b.expst[0]
	send_byte = len(ust.posix.dumps(0))
	recv_byte = len(ust.posix.dumps(1))
	payload = get_rop_payload(my_gadget)
	code.interact(local=locals())

if __name__ == "__main__":
	main()
