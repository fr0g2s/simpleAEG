import angr
import claripy
import sys

binName = "./sample_x86"
input1 = claripy.BVS("input1", 8*0x100)

proj = angr.Project(binName, load_options={"auto_load_libs":False})
state = proj.factory.entry_state(stdin=angr.SimFile("/dev/stdin", content=input1))
for b in input1.chop(8):
    state.add_constraints(b != 0)

simgr = proj.factory.simulation_manager(state, save_unconstrained=True)

try:
    while len(simgr.unconstrained) == 0:
        simgr.step()
        if len(simgr.deadended) > 0:
            for st in simgr.deadended:
                crash_input = st.solver.eval(input1, cast_to=bytes)
                print("== deadended ==")
                print(crash_input)
                print("===============")
except Exception as e:
    print("cancled explore")
    print(e)

if len(simgr.unconstrained) > 0:
    cnt = 0
    for ust in simgr.unconstrained:
        crash_input = ust.solver.eval(input1, cast_to=bytes)
        with open(f'./crash_input_%d' % cnt, 'wb') as f:
            f.write(crash_input)
    print('[*] crash input generation complete')
else:
    print("[!] exploitable state not found")

