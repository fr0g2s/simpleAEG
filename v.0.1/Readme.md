stdin에서 stack-based bof가 발생할 시, crash가 나는 입력값 찾는 스크립트.


## 타겟
arch: **x86** ~~AMD64~~ ELF  
mitigation: None  
section: stack  

## 해야할 것
심볼릭 데이터를 생성하기 위해 길이를 설정해줘야함. (claripy.BVS의 인자)  
소스코드를 파싱하던가, 바이너리를 디스어셈블 하던가, 해서 해당 바이너리에서 사용하는 버퍼의 최대 길이(AEG논문 참고)를 구해서 적용하기?  
아직은 crash만 발생하는 입력값임. 이걸 exploit으로 만들어야함.  
crash가 발생하는 해당 입력값이 exploitable한지 검사를 어떻게 할까?  
  
  
## 사용법
```
$ python find_vuln.py
```

## 구성 요소
- bugFinder.py: 타겟 바이너리를 기호 실행을 통해 버그 탐색
- exploitGen.py: bugFinder.py에서 찾은 버그로 익스플로잇 생성  
- verifier.py: exploitGen.py에서 생성한 페이로드 검증  

나머지는 테스트용 스크립트  
