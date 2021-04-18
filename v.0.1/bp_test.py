# bp걸면 ipdb가 실행된다.
# ipdb는 파이썬 코드 디버거다. angr 내부 코드를 보여준다.
# 바이너리 런타임 정보를 보려면 bp 추가할 때, action 인자를 사용해서 디버깅 함수를 이용해야할 것 같다.
import angr, claripy

def debug_func(state):
    print('='*10)
    print(state.callstack)

proj = angr.Project("./sample", load_options={"auto_load_libs": False})
input1 = claripy.BVS("input1", 8*0x100)
st = proj.factory.call_state(0x4011bb, stdin=angr.SimFile('/dev/stdin', input1))
for b in input1.chop(8):
    st.solver.add(b!=0)
st.inspect.b('mem_write', when=angr.BP_AFTER, action=debug_func)

simgr = proj.factory.simulation_manager(st, save_unconstrained=True)

while len(simgr.unconstrained) == 0:
    simgr.step()

print('[*] data: ', simgr.unconstrained[0].solver.eval(input1))

