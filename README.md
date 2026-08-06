Codyssey Pre-course E1-1: 내 컴퓨터에 개발자용 '작업실' 꾸미기
프로젝트 개요
이 저장소는 코디세이 프리코스 미션 E1-1의 결과물이다. 터미널·Git·Docker라는 개발의 기본 도구를 직접 손으로 세팅해서, 코드가 "내 컴퓨터에서만" 동작하는 문제 없이 누구나 같은 방식으로 실행·배포·디버깅할 수 있는 재현 가능한 개발 환경을 만드는 것이 이 미션의 목표다. 아래 문서는 그 과정에서 실제로 수행한 명령·결과·증거를 기록한 것이다.

수행 항목 체크리스트
 터미널 기본 조작 (pwd/ls/cd/mkdir/touch/rm/cp/mv/cat) — 1. 터미널
 파일 1개 + 디렉토리 1개 권한 변경 실습 — 1. 터미널
 SSH 키 생성 및 GitHub 등록, git clone 인증 — 2. Git
 Git 사용자 정보 설정 (git config --list) — 2. Git
 GitHub 로그인 및 VSCode 연동 — 2. Git
 Docker 설치 및 데몬 점검 (docker info) — 3. Docker
 Docker 기본 운영 명령 (docker images, docker ps -a, docker logs, docker stats) — 3. Docker
 hello-world 실행, ubuntu 컨테이너 진입, exec vs attach 차이 관찰 — 3. Docker
 Dockerfile 기반 커스텀 이미지 빌드/실행 — 3. Docker
 포트 매핑 접속 확인(정상 케이스 + 충돌 케이스) — 3. Docker
 바인드 마운트 반영 확인 — 3. Docker
 Docker 볼륨 영속성 검증(컨테이너 삭제 전/후 비교) — 3. Docker
 트러블슈팅 2건 이상 기록 — 4. 트러블슈팅
검증 방법
항목	검증 명령/방법	결과 위치
터미널 조작	pwd, ls/-a/-l/-la, mkdir, cp, mv, rm 실행 로그	1. 터미널
권한 변경	chmod 전/후 ls -l 비교 (파일 test.txt, 디렉토리 v2)	1. 터미널
SSH 인증	키 없을 때 git clone 실패(Permission denied) → ssh-keygen → GitHub 등록 → 재시도 성공	2. Git
Git 사용자 설정	git config --list 설정 전/후 비교, git log author 비교	2. Git
GitHub 반영	git push 후 커밋 해시를 GitHub 웹 페이지 스크린샷과 대조	2. Git
GitHub/VSCode 연동	VSCode Accounts 메뉴에 GitHub 계정으로 로그인된 상태 스크린샷	2. Git
Docker 설치·데몬 점검	docker info (CLI 미연결 / 정상 / 데몬 다운, 세 가지 케이스 비교)	3. Docker
컨테이너 상태 전이	docker pull→create→start 후 docker ps -a의 STATUS 변화(Created→Exited)	3. Docker
이미지·컨테이너 삭제 순서	docker rmi 실패(must be forced) → docker rm 후 재시도 성공	3. Docker
exec vs attach	둘 다 exit한 뒤 docker ps -a 상태 비교(Up 유지 vs Exited)	3. Docker
커스텀 이미지 빌드	docker build 로그(FINISHED) + docker images에 my-web:1.0 등록 확인	3. Docker
포트 매핑	curl localhost:8080/8082 응답 + docker ps -a의 PORTS 컬럼	3. Docker
포트 충돌	동일 포트 재사용 시 port is already allocated 에러 + 컨테이너가 Created로만 남는 것	3. Docker
로그·리소스 확인	docker logs에 curl 접속 기록 포함 확인, docker stats --no-stream 출력	3. Docker
바인드 마운트	컨테이너 안에서 추가한 줄이 호스트 bind-test/data.txt에도 그대로 반영되는지 cat으로 비교	3. Docker
볼륨 영속성	vol-c 삭제 후 vol-c2에 같은 볼륨 재연결 → cat으로 데이터 유지 확인	3. Docker
0. 실행 환경
항목	값
OS	macOS 15.7.4
Shell	zsh 5.9
터미널	Terminal.app
Git	2.53.0
Docker	28.5.2
1. 터미널
터미널은 마우스로 아이콘을 클릭하는 대신 텍스트로 된 명령어를 직접 입력해서 컴퓨터에게 일을 시키는 창구다. 화면에 보이는 GUI(파인더, 탐색기 같은) 뒤에서 실제로 파일을 읽고 쓰고, 프로그램을 실행하고, 시스템을 설정하는 것도 결국 같은 명령어들인데, 터미널은 그걸 눈에 보이는 클릭 대신 텍스트로 직접 실행하는 방식이다. 이번 실습에서는 파일/디렉토리를 만들고 지우고 옮기고 권한을 바꾸는 기본 명령어들을 하나씩 직접 쳐보면서 익힌다.

아래 표는 이 글에서 실습한 명령어를 정리한 것이다. 가운데 열은 그 명령어가 원래 하는 일이고, 오른쪽 열은 그걸 이 글의 실습 로그에서 실제로 눈으로 확인한 내용이다. 자세한 과정은 각 블록의 로그에서 확인할 수 있다.

명령어	하는 동작	실습에서 확인한 것
pwd	지금 작업 중인 위치를 절대 경로로 출력	cd로 위치를 옮길 때마다 지금 서 있는 곳이 절대 경로로 정확히 바뀌어 찍히는 것
ls / -a / -l / -la	디렉토리 안의 항목을 나열 (옵션에 따라 숨김 파일·상세정보 추가)	옵션이 하나씩 붙을 때마다 숨김 파일 개수, 권한·용량·시각 같은 정보가 얼마나 더 드러나는지
cd	다른 디렉토리로 이동	상대 경로(Desktop, ..)·절대 경로(/Users/...)·~로 각각 이동해봤고, 특히 v1은 상대 경로(cd v1)와 절대 경로(cd /Users/.../v1) 두 방식 모두로 도달 가능함을 비교한 것
mkdir	새 디렉토리 생성	workspace, v0, v1, v2처럼 필요할 때마다 실습용 디렉토리를 그 자리에서 만들어 쓴 것
touch	빈 파일 생성 (이미 있으면 수정 시각만 갱신)	갓 만든 파일의 용량이 정확히 0바이트로 잡힌다는 것
rm / rm -r	파일 삭제 / 디렉토리까지 재귀적으로 삭제	파일은 rm으로, 디렉토리는 rm -r으로 각각 지운 뒤 ls로 비어있는 걸 확인한 것
echo "..." >	파일에 문자열을 새로 씀 (기존 내용은 덮어씀)	써넣은 만큼(개행 포함 6바이트) 파일 용량이 실제로 늘어나는 것
cat	파일 내용을 화면에 그대로 출력	파일 안에 진짜로 어떤 내용이 들어있는지 눈으로 직접 확인한 것
cp	대상이 파일명이면 새 이름으로 복사, 디렉토리면 그 안에 원래 이름 그대로 복사	복사 후에도 원본이 그대로 남아있는 것을 cat으로 원본·사본 둘 다 재확인
mv	대상이 파일명이면 이름 변경, 디렉토리면 그 안으로 이동	디렉토리로 옮길 때는 이동, 파일명으로 줄 때는 이름 변경이라는 걸 두 상황 다 실험
chmod	파일/디렉토리 권한을 8진수로 변경	8진수 한 자리가 rwx 세 비트에 그대로 대응한다는 것, 디렉토리에서 x가 없으면 cd 자체가 막힌다는 것
터미널을 새로 켜면 기본 위치가 홈 디렉토리(~)로 잡힌다. pwd(print working directory)는 지금 내가 있는 위치를 절대 경로로 알려주는 명령어인데, 실행해보면 홈 디렉토리의 절대 경로가 /Users/qwera19976266라는 걸 확인할 수 있다.

qwera19976266@c3r5s4 ~ % pwd
/Users/qwera19976266
이제 홈 디렉토리 안에 뭐가 들어있는지 본다. ls(list)는 기본적으로 점(.)으로 시작하는 숨김 파일은 보여주지 않기 때문에 눈에 보이는 폴더들만 나온다. -a 옵션을 주면 숨김 파일까지 전부 나오고(.claude, .ssh, .zshrc 등), -l 옵션을 주면 각 항목의 권한·소유자·용량·수정 시각 같은 상세 정보가 함께 나온다. 마지막으로 -la는 두 옵션을 합쳐서 숨김 파일까지 상세 정보로 보여준다. ls -a에서 센 항목 수(23개)와 ls -la에서 실제로 출력된 줄 수가 그대로 맞아떨어지는 것도 확인할 수 있다.

qwera19976266@c3r5s4 ~ % ls
Applications	Desktop		Documents	Downloads	Library		Movies		Music		Pictures	Public

qwera19976266@c3r5s4 ~ % ls -a
.			.claude			.ssh			.zsh_sessions		Documents		Music
..			.claude.json		.Trash			.zshrc			Downloads		Pictures
.cache			.copilot		.vscode			Applications		Library			Public
.CFUserTextEncoding	.local			.zsh_history		Desktop			Movies

qwera19976266@c3r5s4 ~ % ls -l
total 0
drwxr-xr-x   3 qwera19976266  qwera19976266    96  8  5 12:39 Applications
drwx------+  8 qwera19976266  qwera19976266   256  8  5 12:47 Desktop
drwx------+  3 qwera19976266  qwera19976266    96  8  5 12:29 Documents
drwx------+  3 qwera19976266  qwera19976266    96  8  5 12:29 Downloads
drwx------@ 76 qwera19976266  qwera19976266  2432  8  5 12:37 Library
drwx------   3 qwera19976266  qwera19976266    96  8  5 12:29 Movies
drwx------+  3 qwera19976266  qwera19976266    96  8  5 12:29 Music
drwx------+  4 qwera19976266  qwera19976266   128  8  5 12:29 Pictures
drwxr-xr-x+  4 qwera19976266  qwera19976266   128  8  5 12:29 Public

qwera19976266@c3r5s4 ~ % ls -la
total 112
drwxr-x---+ 23 qwera19976266  qwera19976266    736  8  5 15:41 .
drwxr-xr-x   6 root           admin            192  8  5 12:29 ..
drwxr-xr-x   3 qwera19976266  qwera19976266     96  8  5 12:37 .cache
-r--------   1 qwera19976266  qwera19976266      8  8  5 12:29 .CFUserTextEncoding
drwxr-xr-x  17 qwera19976266  qwera19976266    544  8  5 15:38 .claude
-rw-------   1 qwera19976266  qwera19976266  41021  8  5 15:39 .claude.json
drwx------   3 qwera19976266  qwera19976266     96  8  5 12:32 .copilot
drwxr-xr-x   5 qwera19976266  qwera19976266    160  8  5 12:37 .local
drwx------   6 qwera19976266  qwera19976266    192  8  5 12:49 .ssh
drwx------+  2 qwera19976266  qwera19976266     64  8  5 12:30 .Trash
drwxr-xr-x   5 qwera19976266  qwera19976266    160  8  5 12:31 .vscode
-rw-------   1 qwera19976266  qwera19976266    305  8  5 15:39 .zsh_history
drwx------   7 qwera19976266  qwera19976266    224  8  5 15:41 .zsh_sessions
-rw-r--r--   1 qwera19976266  qwera19976266     37  8  5 12:37 .zshrc
drwxr-xr-x   3 qwera19976266  qwera19976266     96  8  5 12:39 Applications
drwx------+  8 qwera19976266  qwera19976266    256  8  5 12:47 Desktop
drwx------+  3 qwera19976266  qwera19976266     96  8  5 12:29 Documents
drwx------+  3 qwera19976266  qwera19976266     96  8  5 12:29 Downloads
drwx------@ 76 qwera19976266  qwera19976266   2432  8  5 12:37 Library
drwx------   3 qwera19976266  qwera19976266     96  8  5 12:29 Movies
drwx------+  3 qwera19976266  qwera19976266     96  8  5 12:29 Music
drwx------+  4 qwera19976266  qwera19976266    128  8  5 12:29 Pictures
drwxr-xr-x+  4 qwera19976266  qwera19976266    128  8  5 12:29 Public
-l 출력은 한 줄에 정보가 여러 개 붙어 있어서 처음엔 헷갈리는데, 위 Applications 줄(drwxr-xr-x   3 qwera19976266  qwera19976266    96  8  5 12:39 Applications)을 기준으로 순서대로 뜯어보면 이렇다.

순서	값	의미
①	drwxr-xr-x	타입 + 권한. 첫 글자가 타입(d=디렉토리, -=일반 파일), 이후 9자리가 소유자/그룹/기타 사용자의 읽기(r)·쓰기(w)·실행(x) 권한
②	3	링크 수
③	qwera19976266	소유자
④	qwera19976266	소유 그룹
⑤	96	크기
⑥	8  5 12:39	마지막 수정 시각
⑦	Applications	이름
이제 실습을 진행할 위치로 이동한다. cd(change directory)로 이동하는데, cd Desktop은 지금 위치(홈 디렉토리)를 기준으로 한 상대 경로 이동이다. 이동한 뒤 pwd로 실제로 어디 와 있는지 절대 경로로 다시 확인하고, ls로 Desktop 안에 뭐가 있는지 본다. 여기에 앞으로 실습 전용으로 쓸 디렉토리를 하나 만들기 위해 mkdir(make directory) workspace를 실행하고, 다시 ls로 workspace가 새로 생겼는지 확인한다.

qwera19976266@c3r5s4 ~ % cd Desktop

qwera19976266@c3r5s4 Desktop % pwd
/Users/qwera19976266/Desktop

qwera19976266@c3r5s4 Desktop % ls
github									스크린샷 2026-08-05 오후 12.47.35.png
스크린샷 2026-08-05 오후 12.47.14.png					스크린샷 2026-08-05 오후 12.47.49.png

qwera19976266@c3r5s4 Desktop % mkdir workspace

qwera19976266@c3r5s4 Desktop % ls
github									스크린샷 2026-08-05 오후 12.47.35.png
workspace								스크린샷 2026-08-05 오후 12.47.49.png
스크린샷 2026-08-05 오후 12.47.14.png
workspace로 들어가서(cd workspace) 본격적으로 파일과 디렉토리를 만들고 지워본다. 먼저 pwd로 위치를 확인하고 ls로 비어있는 걸 확인한다. touch test.txt로 빈 파일을 하나 만들고 ls로 생겼는지 확인한 다음, rm(remove) test.txt로 지우고 다시 비어있는지 본다. 같은 흐름을 디렉토리에도 적용해본다. mkdir test로 디렉토리를 만들고, 지울 때는 rm test가 아니라 rm -r test를 써야 한다. rm은 파일 삭제용이라 디렉토리에는 통하지 않고, 지금처럼 비어 있는 디렉토리라도 재귀적으로(-r, recursive) 지워야 한다.

qwera19976266@c3r5s4 Desktop % cd workspace

qwera19976266@c3r5s4 workspace % pwd
/Users/qwera19976266/Desktop/workspace

qwera19976266@c3r5s4 workspace % ls

qwera19976266@c3r5s4 workspace % touch test.txt

qwera19976266@c3r5s4 workspace % ls
test.txt

qwera19976266@c3r5s4 workspace % rm test.txt

qwera19976266@c3r5s4 workspace % ls

qwera19976266@c3r5s4 workspace % mkdir test

qwera19976266@c3r5s4 workspace % ls
test

qwera19976266@c3r5s4 workspace % rm -r test

qwera19976266@c3r5s4 workspace % ls
이번엔 파일 안에 실제 내용을 넣어보고 그게 용량에 어떻게 반영되는지 확인한다. touch test.txt로 빈 파일을 만들면 ls -l에서 용량이 0바이트로 나온다. 여기에 echo(입력한 문자열을 그대로 따라 출력한다는 뜻) "hello" > test.txt로 문자열을 써넣으면(>는 파일 내용을 덮어쓰는 리다이렉션이다) 다시 ls -l을 찍었을 때 용량이 6바이트로 늘어난 걸 볼 수 있다. hello는 글자 수로는 5자지만 echo가 줄 끝에 개행 문자(\n)를 하나 더 붙이기 때문에 총 6바이트가 된다. 마지막으로 cat(concatenate) test.txt로 실제 내용이 hello인지 확인한다.

qwera19976266@c3r5s4 workspace % touch test.txt

qwera19976266@c3r5s4 workspace % ls -l
total 0
-rw-r--r--  1 qwera19976266  qwera19976266  0  8  5 15:52 test.txt

qwera19976266@c3r5s4 workspace % echo "hello" > test.txt

qwera19976266@c3r5s4 workspace % ls -l
total 8
-rw-r--r--  1 qwera19976266  qwera19976266  6  8  5 15:52 test.txt

qwera19976266@c3r5s4 workspace % cat test.txt
hello
이제 복사와 이동을 구분해서 실습한다. 먼저 mkdir v0로 디렉토리를 하나 만들고, cp(copy) test.txt test_backup.txt로 test.txt를 다른 이름으로 복사한다. cp는 복사이기 때문에 원본(test.txt)과 사본(test_backup.txt) 둘 다 남아있고, cat으로 둘 다 내용이 hello로 같은 것도 확인한다. 그다음 mv(move) test_backup.txt v0를 실행하는데, 두 번째 인자가 파일명이 아니라 이미 존재하는 디렉토리(v0)이기 때문에 이건 이름 변경이 아니라 "v0 안으로 이동"하는 동작이 된다. mv는 이동이라 원본은 workspace에 남지 않고 사라지며, cd v0 후 ls로 실제로 그 안에 들어가 있는 걸 확인한다.

qwera19976266@c3r5s4 workspace % mkdir v0

qwera19976266@c3r5s4 workspace % ls
test.txt	v0

qwera19976266@c3r5s4 workspace % cp test.txt test_backup.txt

qwera19976266@c3r5s4 workspace % ls
test_backup.txt	test.txt	v0

qwera19976266@c3r5s4 workspace % cat test.txt
hello

qwera19976266@c3r5s4 workspace % cat test_backup.txt
hello

qwera19976266@c3r5s4 workspace % mv test_backup.txt v0

qwera19976266@c3r5s4 workspace % ls
test.txt	v0

qwera19976266@c3r5s4 workspace % cd v0

qwera19976266@c3r5s4 v0 % ls
test_backup.txt
이번엔 mv를 이름 변경 용도로 써본다. v0 안에서 mv test_backup.txt test_v0.txt를 실행하면, 두 번째 인자가 존재하는 디렉토리가 아니라 새로운 파일명이기 때문에 파일을 다른 위치로 옮기는 게 아니라 이름만 바뀐다. cd ..로 다시 workspace로 나온 뒤, mkdir v1로 디렉토리를 하나 더 만들고 cp test.txt v1로 이번엔 복사를 해서 넣는다. cp이기 때문에 workspace의 test.txt는 그대로 남아있고, cd v1과 cat test.txt로 복사본 안에도 원본과 같은 내용(hello)이 들어있는 걸 확인한다.

qwera19976266@c3r5s4 v0 % mv test_backup.txt test_v0.txt

qwera19976266@c3r5s4 v0 % ls
test_v0.txt

qwera19976266@c3r5s4 v0 % cd ..

qwera19976266@c3r5s4 workspace % ls
test.txt	v0

qwera19976266@c3r5s4 workspace % mkdir v1

qwera19976266@c3r5s4 workspace % ls
test.txt	v0		v1

qwera19976266@c3r5s4 workspace % cp test.txt v1

qwera19976266@c3r5s4 workspace % ls
test.txt	v0		v1

qwera19976266@c3r5s4 workspace % cd v1

qwera19976266@c3r5s4 v1 % ls
test.txt

qwera19976266@c3r5s4 v1 % cat test.txt
hello
이제 파일 권한을 다뤄본다. ls -l에서 맨 앞의 -rw-r--r-- 같은 문자열이 권한을 나타내는데, 첫 글자 -는 일반 파일이라는 뜻이고(디렉토리면 d) 이후 9칸이 소유자/그룹/그 외 사용자 순서로 각각 읽기(r)·쓰기(w)·실행(x) 권한 여부를 나타낸다. chmod(change mode) 755 test.txt를 실행하면 권한이 rwxr-xr-x로 바뀌는데, 8진수 한 자리가 rwx 세 비트에 그대로 대응한다(7=rwx, 5=r-x). 즉 소유자에게는 실행 권한까지 주고, 그룹과 기타 사용자에게는 읽기+실행만 준 것이다. 다시 chmod 644 test.txt로 되돌리면 rw-r--r--가 되어 아무도 실행 권한이 없는 원래 상태로 돌아온다.

qwera19976266@c3r5s4 v1 % ls -l
total 8
-rw-r--r--  1 qwera19976266  qwera19976266  6  8  5 15:57 test.txt

qwera19976266@c3r5s4 v1 % chmod 755 test.txt

qwera19976266@c3r5s4 v1 % ls -l
total 8
-rwxr-xr-x  1 qwera19976266  qwera19976266  6  8  5 15:57 test.txt

qwera19976266@c3r5s4 v1 % chmod 644 test.txt

qwera19976266@c3r5s4 v1 % ls -l
total 8
-rw-r--r--  1 qwera19976266  qwera19976266  6  8  5 15:57 test.txt
디렉토리도 파일과 똑같이 권한을 가지는데, 디렉토리에서는 실행(x) 권한의 의미가 다르다. 디렉토리에 x 권한이 없으면 그 안으로 들어가거나(cd) 안에 있는 항목에 접근할 수 없다. 이걸 직접 확인해보기 위해 cd ..로 workspace로 나온 뒤 mkdir v2로 새 디렉토리를 만든다. ls -l을 보면 mkdir로 갓 만든 디렉토리는 기본적으로 drwxr-xr-x(755) 권한을 갖는다(v0, v1도 마찬가지). 여기에 chmod 644 v2를 실행해서 실행 권한을 모두 제거하면 drw-r--r--로 바뀐다. 이 상태에서 cd v2를 시도하면 cd: permission denied: v2라는 에러가 나는데, 이게 바로 디렉토리에서 x 권한이 왜 필요한지 보여주는 실습이다.

qwera19976266@c3r5s4 v1 % cd ..

qwera19976266@c3r5s4 workspace % ls
test.txt	v0		v1

qwera19976266@c3r5s4 workspace % mkdir v2

qwera19976266@c3r5s4 workspace % ls -l
total 8
-rw-r--r--  1 qwera19976266  qwera19976266   6  8  5 15:52 test.txt
drwxr-xr-x  3 qwera19976266  qwera19976266  96  8  5 15:57 v0
drwxr-xr-x  3 qwera19976266  qwera19976266  96  8  5 15:57 v1
drwxr-xr-x  2 qwera19976266  qwera19976266  64  8  5 16:06 v2

qwera19976266@c3r5s4 workspace % chmod 644 v2

qwera19976266@c3r5s4 workspace % ls -l
total 8
-rw-r--r--  1 qwera19976266  qwera19976266   6  8  5 15:52 test.txt
drwxr-xr-x  3 qwera19976266  qwera19976266  96  8  5 15:57 v0
drwxr-xr-x  3 qwera19976266  qwera19976266  96  8  5 15:57 v1
drw-r--r--  2 qwera19976266  qwera19976266  64  8  5 16:06 v2

qwera19976266@c3r5s4 workspace % cd v2
cd: permission denied: v2
마지막으로 절대 경로와 상대 경로를 명확히 구분해서 정리한다. cd ~는 물결표(~)로 홈 디렉토리로 바로 이동하는 단축 표현이다. 이어서 cd Desktop/workspace는 여러 단계를 한 번에 내려가는 상대 경로이고(지금 위치인 홈을 기준으로 한다), cd ../..는 ..(상위 디렉토리)를 두 번 이어 써서 두 단계 위, 즉 다시 홈으로 올라가는 상대 경로다. 마지막으로 cd /Users/qwera19976266/Desktop/workspace/v1처럼 루트(/)에서 시작하는 절대 경로를 쓰면, 지금 어디에 있든 상관없이 항상 같은 대상을 가리킨다. 실제로 홈 디렉토리(~)에서 중간 경로를 거치지 않고 절대 경로 한 줄만으로 곧장 v1까지 이동한 걸 pwd 결과로 확인할 수 있다.

qwera19976266@c3r5s4 workspace % cd ~

qwera19976266@c3r5s4 ~ % pwd
/Users/qwera19976266

qwera19976266@c3r5s4 ~ % cd Desktop/workspace

qwera19976266@c3r5s4 workspace % pwd
/Users/qwera19976266/Desktop/workspace

qwera19976266@c3r5s4 workspace % cd ../..

qwera19976266@c3r5s4 ~ % pwd
/Users/qwera19976266

qwera19976266@c3r5s4 ~ % cd /Users/qwera19976266/Desktop/workspace/v1

qwera19976266@c3r5s4 v1 % pwd
/Users/qwera19976266/Desktop/workspace/v1
2. Git
Git은 파일이 바뀌어온 과정을 스냅샷(커밋) 단위로 기록해두는 버전 관리 도구다. 파일을 고칠 때마다 그냥 덮어써버리면 예전 상태로 돌아가거나 언제 뭐가 바뀌었는지 알 방법이 없는데, Git은 변경 하나하나를 이력으로 쌓아두기 때문에 언제든 과거 시점을 다시 볼 수 있고 무엇이 왜 바뀌었는지도 추적할 수 있다. 이 이력은 기본적으로 지금 이 컴퓨터 안(로컬 저장소)에만 존재한다. GitHub은 이 로컬 저장소를 인터넷의 원격 저장소로 올려서 백업해두거나, 다른 컴퓨터·다른 사람과 같은 이력을 주고받을 수 있게 해주는 호스팅 서비스다. 로컬과 원격 사이를 오갈 때 방향에 따라 부르는 이름도 다른데, 원격 저장소를 통째로 로컬로 가져오는 게 clone, 로컬에서 만든 커밋을 원격으로 올리는 게 push다.

로컬과 원격을 오가려면 먼저 GitHub에게 "이 컴퓨터가 내 계정이 맞다"는 걸 증명해야 하는데, 이번 실습은 그 인증부터 막히는 상황(SSH 키가 없어서 git clone이 실패하는 것)을 겪고, 키를 새로 만들어 등록한 뒤에야 저장소를 내려받아 커밋하고 push까지 이어가는 흐름을 따라간다.

아래 표는 이 글에서 실습한 명령어를 정리한 것이다. cd·mkdir·ls·touch·cat처럼 앞서 터미널 편에서 이미 다룬 명령어는 여기서는 뺐다.

명령어	하는 동작	실습에서 확인한 것
git clone	원격 저장소를 통째로 복제해서 로컬로 가져옴	SSH 키가 없을 때는 Permission denied (publickey)로 실패하고, 키를 등록한 뒤 재시도하면 성공하는 것을 직접 비교
ssh-keygen	공개키·개인키 쌍을 새로 생성	생성 전엔 ~/.ssh에 known_hosts만 있다가, 생성 후 id_ed25519(개인키)·id_ed25519.pub(공개키) 두 파일이 생기는 것
git status	작업 디렉토리의 추적·변경 상태 확인	파일을 만들기 전 / add 전 / add 후, 세 시점마다 상태 문구가 바뀌는 것
git add	변경 사항을 커밋 대상(Staging Area)에 올림	add 전엔 "추적하지 않는 파일"이던 게 add 후엔 "커밋할 변경 사항"으로 옮겨가는 것
git commit -m	Staging Area의 내용을 저장소에 커밋으로 기록	사용자 정보를 설정하기 전이라 시스템이 자동 추정한 이름·이메일로 커밋되고, 그걸 경고 메시지로 알려주는 것
git log	커밋 이력(해시·작성자·시각·메시지) 확인	git config로 사용자 정보를 나중에 바꿔도 이미 만든 커밋의 author는 그대로 남아있다는 걸 log를 두 번 찍어 비교한 것
git config	Git 설정값을 확인·변경	--list로 처음엔 user.name/user.email이 아예 없는 걸 확인하고, 설정 후 다시 --list로 반영된 걸 확인한 것
git commit --amend	가장 최근 커밋의 내용은 두고 일부만 바꿔 다시 씀	--author로 잘못 기록된 작성자를 고친 뒤, 커밋 해시가 바뀌면서 log의 author도 함께 바뀌는 것을 확인한 것
git push	로컬 커밋을 원격 저장소로 올림	push 후 GitHub 웹 페이지(스크린샷)에서 실제로 같은 커밋 해시가 올라온 걸 확인한 것
실습을 진행할 위치부터 만든다. cd Desktop으로 이동한 뒤 mkdir github로 저장소를 담을 디렉토리를 만들고 cd github로 그 안에 들어간다.

qwera19976266@c3r5s4 ~ % ls
Desktop		Downloads	Movies		Pictures
Documents	Library		Music		Public

qwera19976266@c3r5s4 ~ % cd Desktop

qwera19976266@c3r5s4 Desktop % ls

qwera19976266@c3r5s4 Desktop % mkdir github

qwera19976266@c3r5s4 Desktop % cd github

qwera19976266@c3r5s4 github % ls
이 디렉토리 안에서 git clone으로 원격 저장소를 그대로 복제해본다. 주소가 git@github.com:...로 시작하는 SSH 방식인데, 아직 이 컴퓨터에 등록된 SSH 키가 없어서 Permission denied (publickey)로 실패한다. GitHub에게 "이 컴퓨터가 내 계정이 맞다"는 걸 증명할 키가 없으니 접근 자체가 막히는 것이다.

qwera19976266@c3r5s4 github % git clone git@github.com:FickleBoBo/Codyssey-Pre-course-E1-1.git
'Codyssey-Pre-course-E1-1'에 복제합니다...
The authenticity of host 'github.com (20.200.245.247)' can't be established.
ED25519 key fingerprint is SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'github.com' (ED25519) to the list of known hosts.
git@github.com: Permission denied (publickey).
fatal: 리모트 저장소에서 읽을 수 없습니다

올바른 접근 권한이 있는지, 그리고 저장소가 있는지
확인하십시오.
실패한 이유를 확인하기 위해 ~/.ssh 디렉토리를 들여다본다. ~/.ssh는 SSH 키를 비롯한 인증 관련 파일들이 모이는 표준 위치인데, 지금은 known_hosts(방금 git clone 과정에서 GitHub 서버를 처음 신뢰하면서 자동으로 기록된 파일) 하나만 있고 인증에 쓸 키 파일은 아직 없다.

qwera19976266@c3r5s4 github % ls -la ~/.ssh
total 8
drwx------   3 qwera19976266  qwera19976266   96  8  5 12:37 .
drwxr-x---+ 22 qwera19976266  qwera19976266  704  8  5 12:42 ..
-rw-r--r--   1 qwera19976266  qwera19976266   92  8  5 12:37 known_hosts
ssh-keygen -t ed25519 -C "test"로 새 키 쌍을 만든다. -t ed25519는 키 알고리즘 종류를 지정하는 것이고 -C는 키에 달아둘 설명(comment)이다. 저장 경로와 암호는 그냥 엔터로 넘겨서 기본값(~/.ssh/id_ed25519, 암호 없음)으로 생성한다.

qwera19976266@c3r5s4 github % ssh-keygen -t ed25519 -C "test"
Generating public/private ed25519 key pair.
Enter file in which to save the key (/Users/qwera19976266/.ssh/id_ed25519):
Enter passphrase for "/Users/qwera19976266/.ssh/id_ed25519" (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /Users/qwera19976266/.ssh/id_ed25519
Your public key has been saved in /Users/qwera19976266/.ssh/id_ed25519.pub
The key fingerprint is:
SHA256:hyzIPCXrtaUWlRZgx3vBHpkDrUzebdYONmjIYdB87eU test
The key's randomart image is:
+--[ED25519 256]--+
|      +*++ +     |
|     . .BoX . .  |
|    . .*+O B +   |
|   o = +B.* O E  |
|    * + So.+ +   |
|   . o * .    .  |
|    . +          |
|     .           |
|                 |
+----[SHA256]-----+
다시 ~/.ssh를 보면 id_ed25519(개인키)와 id_ed25519.pub(공개키) 두 파일이 새로 생긴 걸 확인할 수 있다. 이 중 GitHub에 등록해야 하는 건 공개키 쪽이라 cat id_ed25519.pub로 내용을 출력해서 복사할 준비를 한다.

qwera19976266@c3r5s4 github % ls -la ~/.ssh
total 24
drwx------   5 qwera19976266  qwera19976266  160  8  5 12:46 .
drwxr-x---+ 22 qwera19976266  qwera19976266  704  8  5 12:45 ..
-rw-------   1 qwera19976266  qwera19976266  387  8  5 12:46 id_ed25519
-rw-r--r--   1 qwera19976266  qwera19976266   86  8  5 12:46 id_ed25519.pub
-rw-r--r--   1 qwera19976266  qwera19976266   92  8  5 12:37 known_hosts

qwera19976266@c3r5s4 github % cat ~/.ssh/id_ed25519.pub
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICxQ0JndiJjd86kmQjtRU3uzz2RyLq4lu5RYkUMaNJvS test
이 공개키를 GitHub 계정의 SSH 설정 페이지(github.com/settings/keys)에 등록한다.

SSH 키 등록 전, 기존 키만 있는 GitHub SSH keys 설정 페이지

방금 출력한 공개키를 붙여넣은 Add new SSH Key 화면

등록 완료 후, 새 키가 목록에 추가된 SSH keys 설정 페이지

키를 등록한 뒤 같은 git clone 명령을 다시 실행하면 이번엔 인증을 통과해서 저장소가 실제로 복제된다. 이때 내부적으로는 SSH 클라이언트가 ~/.ssh에 있는 개인키로 GitHub 서버가 보낸 값에 서명을 하고, GitHub은 그 서명을 계정에 등록된 공개키로 검증하는 방식으로 인증이 이뤄진다. 개인키 자체는 한 번도 네트워크로 전송되지 않고 이 컴퓨터 안에만 남아있기 때문에, 비밀번호를 매번 입력하지 않고도 인증이 성사되는 것이다.

qwera19976266@c3r5s4 github % git clone git@github.com:FickleBoBo/Codyssey-Pre-course-E1-1.git
'Codyssey-Pre-course-E1-1'에 복제합니다...
remote: Enumerating objects: 28, done.
remote: Counting objects: 100% (28/28), done.
remote: Compressing objects: 100% (17/17), done.
remote: Total 28 (delta 7), reused 28 (delta 7), pack-reused 0 (from 0)
오브젝트를 받는 중: 100% (28/28), 3.35 MiB | 3.01 MiB/s, 완료.
델타를 알아내는 중: 100% (7/7), 완료.

qwera19976266@c3r5s4 github % ls
Codyssey-Pre-course-E1-1
복제된 디렉토리 안으로 들어가서 ls -a로 내용을 확인한다. 눈에 보이는 파일들 사이에 .git이라는 숨김 디렉토리가 있는데, 이게 바로 이 디렉토리를 평범한 폴더가 아니라 "git으로 관리되는 저장소"로 만들어주는 실체다 — 커밋 이력, 설정, 원격 주소 같은 정보가 전부 이 안에 저장돼 있고, 방금 실행한 git clone이 실제로 하는 일도 결국 원격 저장소의 .git 내용을 통째로 복제해오는 것이다. 이어서 git status로 현재 상태를 본다. README2.md가 추적되지 않은(untracked) 파일로 잡히는데, 로컬에서 새로 쓰는 중이라 아직 원격 저장소엔 없는 파일이기 때문이다. 여기에 touch test.txt로 파일을 하나 더 만들고 다시 git status를 보면 추적하지 않는 파일 목록에 test.txt도 추가된다. git add test.txt로 이 파일만 커밋 대상(Staging Area)에 올리면 git status의 표시가 "추적하지 않는 파일"에서 "커밋할 변경 사항"으로 옮겨간다. 마지막으로 git commit -m "test commit"으로 커밋을 만드는데, 이때 Git이 사용자 이름·이메일을 따로 설정한 적이 없어서 컴퓨터 사용자명과 호스트명을 조합해 자동으로 신원을 추정했다는 경고 메시지가 함께 뜬다.

qwera19976266@c3r5s4 github % cd Codyssey-Pre-course-E1-1

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % ls -a
.		..		.git		.gitkeep	assets		docker-practice	practice	README.md	README2.md

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % git status
현재 브랜치 main
브랜치가 'origin/main'에 맞게 업데이트된 상태입니다.

추적하지 않는 파일:
  (커밋할 사항에 포함하려면 "git add <파일>..."을 사용하십시오)
	README2.md

커밋할 사항을 추가하지 않았지만 추적하지 않는 파일이 있습니다 (추적하려면 "git
add"를 사용하십시오)

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % touch test.txt

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % ls
assets		docker-practice	practice	README.md	README2.md	test.txt

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % git status
현재 브랜치 main
브랜치가 'origin/main'에 맞게 업데이트된 상태입니다.

추적하지 않는 파일:
  (커밋할 사항에 포함하려면 "git add <파일>..."을 사용하십시오)
	README2.md
	test.txt

커밋할 사항을 추가하지 않았지만 추적하지 않는 파일이 있습니다 (추적하려면 "git
add"를 사용하십시오)

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % git add test.txt

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % git status
현재 브랜치 main
브랜치가 'origin/main'에 맞게 업데이트된 상태입니다.

커밋할 변경 사항:
  (use "git restore --staged <file>..." to unstage)
	새 파일:       test.txt

추적하지 않는 파일:
  (커밋할 사항에 포함하려면 "git add <파일>..."을 사용하십시오)
	README2.md

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % git commit -m "test commit"
[main bff69ae] test commit
 Committer: 육민우 <qwera19976266@c3r5s4.codyssey.kr>
이름과 전자메일 주소를 사용자 이름과 호스트 이름을 이용해서 자동으로
설정했습니다. 이 정보가 맞는지 확인하십시오. 이 메시지를 보지 않으려면 정보를
명시적으로 설정하십시오. 다음 명령어를 실행하고 편집기의 안내에 따라 설정
파일을 편집하십시오:

    git config --global --edit

이렇게 한 다음, 이 커밋에 사용한 신원 정보를 다음과 같이 해서 바꿀 수 있습니다:

    git commit --amend --reset-author

 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 test.txt
git log로 방금 만든 커밋을 확인하면, 작성자(Author)가 원하는 GitHub 계정이 아니라 방금 경고에서 본 자동 추정 정보로 기록되어 있는 걸 볼 수 있다.

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % git log
commit bff69ae61cfa4c288cfd92ab37b94416d9271a5f (HEAD -> main)
Author: 육민우 <qwera19976266@c3r5s4.codyssey.kr>
Date:   Wed Aug 5 17:08:35 2026 +0900

    test commit

commit 1752d1bef51c92e9d0771638cbd4c8ae82f6ce3b (origin/main, origin/HEAD)
Author: FickleBoBo <yukmw0704@gmail.com>
Date:   Sun Aug 2 17:17:04 2026 +0900

    docs: E1-1 개발 워크스테이션 구축 기술 문서 작성

commit 32d9e79bd15a0e204f959a7e988d76de5824d207
Author: FickleBoBo <yukmw0704@gmail.com>
Date:   Sun Aug 2 17:16:58 2026 +0900

    docs: GitHub/VSCode 연동·포트 매핑·바인드 마운트 증거 스크린샷 추가

commit 2988746d7f4af46b059498ce35cf3debf15bbbbd
Author: FickleBoBo <yukmw0704@gmail.com>
Date:   Sun Aug 2 17:16:47 2026 +0900

    feat: nginx:alpine 기반 커스텀 이미지 소스 추가 (Dockerfile, 정적 페이지)

commit e1222b4d560cd43aab06597471758869da9f298e
Author: FickleBoBo <yukmw0704@gmail.com>
Date:   Sun Aug 2 17:16:36 2026 +0900

    chore: 터미널 조작 및 권한 실습 산출물 추가

commit 40608b97fe08dc6115702c4bf90a9832a6422c64
Author: FickleBoBo <yukmw0704@gmail.com>
Date:   Sun Aug 2 12:55:46 2026 +0900

    test: test commit
git config --list로 현재 이 저장소에 적용된 설정값을 쭉 확인해보면, remote.origin.url이나 branch.main.merge 같은 값은 있어도 user.name·user.email은 목록에 아예 없다. 커밋할 때마다 자동 추정 정보로 기록된 이유가 바로 이거다.

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % git config --list
credential.helper=osxkeychain
core.repositoryformatversion=0
core.filemode=true
core.bare=false
core.logallrefupdates=true
core.ignorecase=true
core.precomposeunicode=true
remote.origin.url=git@github.com:FickleBoBo/Codyssey-Pre-course-E1-1.git
remote.origin.fetch=+refs/heads/*:refs/remotes/origin/*
branch.main.remote=origin
branch.main.merge=refs/heads/main
branch.main.vscode-merge-base=origin/main
git config user.name과 git config user.email로 이 저장소에서 쓸 사용자 정보를 지정한다. 다시 git config --list를 보면 이번엔 목록 맨 아래에 user.name·user.email이 추가된 걸 확인할 수 있다.

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % git config user.name FickleBoBo

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % git config user.email yukmw0704@gmail.com

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % git config --list
credential.helper=osxkeychain
core.repositoryformatversion=0
core.filemode=true
core.bare=false
core.logallrefupdates=true
core.ignorecase=true
core.precomposeunicode=true
remote.origin.url=git@github.com:FickleBoBo/Codyssey-Pre-course-E1-1.git
remote.origin.fetch=+refs/heads/*:refs/remotes/origin/*
branch.main.remote=origin
branch.main.merge=refs/heads/main
branch.main.vscode-merge-base=origin/main
user.name=FickleBoBo
user.email=yukmw0704@gmail.com
하지만 git log를 다시 찍어보면 방금 만든 커밋의 author는 그대로다. git config는 앞으로 만들 커밋에만 적용될 뿐, 이미 만들어진 커밋을 소급해서 고쳐주지는 않기 때문이다. 이걸 고치려면 git commit --amend --author="FickleBoBo <yukmw0704@gmail.com>" --no-edit처럼 직접 지정해서 마지막 커밋을 다시 써야 한다(--no-edit은 커밋 메시지는 그대로 두고 author만 바꾸겠다는 뜻). 실행하면 커밋 해시가 bff69ae에서 5d40653으로 바뀌는데, --amend가 기존 커밋을 그 자리에서 수정하는 게 아니라 내용은 같고 author만 다른 새 커밋으로 대체하는 방식이기 때문이다. 다시 git log로 확인하면 이번엔 author가 원하는 정보로 정확히 찍힌다.

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % git log
commit bff69ae61cfa4c288cfd92ab37b94416d9271a5f (HEAD -> main)
Author: 육민우 <qwera19976266@c3r5s4.codyssey.kr>
Date:   Wed Aug 5 17:08:35 2026 +0900

    test commit

commit 1752d1bef51c92e9d0771638cbd4c8ae82f6ce3b (origin/main, origin/HEAD)
Author: FickleBoBo <yukmw0704@gmail.com>
Date:   Sun Aug 2 17:17:04 2026 +0900

    docs: E1-1 개발 워크스테이션 구축 기술 문서 작성

commit 32d9e79bd15a0e204f959a7e988d76de5824d207
Author: FickleBoBo <yukmw0704@gmail.com>
Date:   Sun Aug 2 17:16:58 2026 +0900

    docs: GitHub/VSCode 연동·포트 매핑·바인드 마운트 증거 스크린샷 추가

commit 2988746d7f4af46b059498ce35cf3debf15bbbbd
Author: FickleBoBo <yukmw0704@gmail.com>
Date:   Sun Aug 2 17:16:47 2026 +0900

    feat: nginx:alpine 기반 커스텀 이미지 소스 추가 (Dockerfile, 정적 페이지)

commit e1222b4d560cd43aab06597471758869da9f298e
Author: FickleBoBo <yukmw0704@gmail.com>
Date:   Sun Aug 2 17:16:36 2026 +0900

    chore: 터미널 조작 및 권한 실습 산출물 추가

commit 40608b97fe08dc6115702c4bf90a9832a6422c64
Author: FickleBoBo <yukmw0704@gmail.com>
Date:   Sun Aug 2 12:55:46 2026 +0900

    test: test commit

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % git commit --amend --author="FickleBoBo <yukmw0704@gmail.com>" --no-edit
[main 5d40653] test commit
 Date: Wed Aug 5 17:08:35 2026 +0900
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 test.txt

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % git log
commit 5d40653efabc98d88e0e4f80ee28bb472838f953 (HEAD -> main)
Author: FickleBoBo <yukmw0704@gmail.com>
Date:   Wed Aug 5 17:08:35 2026 +0900

    test commit

commit 1752d1bef51c92e9d0771638cbd4c8ae82f6ce3b (origin/main, origin/HEAD)
Author: FickleBoBo <yukmw0704@gmail.com>
Date:   Sun Aug 2 17:17:04 2026 +0900

    docs: E1-1 개발 워크스테이션 구축 기술 문서 작성

commit 32d9e79bd15a0e204f959a7e988d76de5824d207
Author: FickleBoBo <yukmw0704@gmail.com>
Date:   Sun Aug 2 17:16:58 2026 +0900

    docs: GitHub/VSCode 연동·포트 매핑·바인드 마운트 증거 스크린샷 추가

commit 2988746d7f4af46b059498ce35cf3debf15bbbbd
Author: FickleBoBo <yukmw0704@gmail.com>
Date:   Sun Aug 2 17:16:47 2026 +0900

    feat: nginx:alpine 기반 커스텀 이미지 소스 추가 (Dockerfile, 정적 페이지)

commit e1222b4d560cd43aab06597471758869da9f298e
Author: FickleBoBo <yukmw0704@gmail.com>
Date:   Sun Aug 2 17:16:36 2026 +0900

    chore: 터미널 조작 및 권한 실습 산출물 추가

commit 40608b97fe08dc6115702c4bf90a9832a6422c64
Author: FickleBoBo <yukmw0704@gmail.com>
Date:   Sun Aug 2 12:55:46 2026 +0900

    test: test commit
마지막으로 git push -u origin main으로 로컬 커밋을 원격 저장소에 올린다. -u는 이후부터 이 브랜치에서 git push만 쳐도 자동으로 origin main을 대상으로 삼도록 추적을 연결하는 옵션이다.

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % git push -u origin main
오브젝트 나열하는 중: 3, 완료.
오브젝트 개수 세는 중: 100% (3/3), 완료.
Delta compression using up to 6 threads
오브젝트 압축하는 중: 100% (2/2), 완료.
오브젝트 쓰는 중: 100% (2/2), 244 bytes | 244.00 KiB/s, 완료.
Total 2 (delta 1), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (1/1), completed with 1 local object.
To github.com:FickleBoBo/Codyssey-Pre-course-E1-1.git
   1752d1b..5d40653  main -> main
branch 'main' set up to track 'origin/main'.
실제로 GitHub 저장소 페이지에서 커밋 목록을 확인하면, 방금 amend로 고친 해시(5d40653)와 올바른 작성자(FickleBoBo)로 커밋이 올라와 있는 걸 볼 수 있다.

GitHub 저장소 커밋 목록에 5d40653 test commit이 FickleBoBo 작성으로 반영된 화면

참고로 VSCode에도 이런 식으로 GitHub 계정을 연동해서 쓸 수 있다. Source Control 계정 메뉴를 열어보면 이 컴퓨터가 GitHub 계정(FickleBoBo)으로 로그인돼 있는 걸 확인할 수 있다. 기존 개인 PC의 VSCode 설정을 동기화를 통해 가져올 수도 있다.

VSCode 계정 메뉴에 GitHub 계정 FickleBoBo로 로그인된 상태

3. Docker
도커는 애플리케이션을 실행에 필요한 라이브러리·설정까지 통째로 묶어서, 어떤 환경에서도 똑같이 돌아가는 격리된 실행 단위(컨테이너)로 만들어주는 도구다. 이미지(image)는 컨테이너를 찍어내는 읽기 전용 템플릿이고, 컨테이너(container)는 그 이미지를 바탕으로 실제로 켜져 있는(또는 켜졌다 멈춘) 인스턴스다. 같은 이미지 하나로 이름만 다른 여러 컨테이너를 동시에 띄울 수 있다는 것도 이번 실습에서 직접 확인했다.

컨테이너는 기본적으로 삭제되면 그 안에 있던 파일도 함께 사라지는 휘발성 저장 공간을 갖는다. 이번 실습은 이미지를 내려받아 컨테이너를 만들고 켜고 끄고 지우는 가장 기본적인 조작부터 시작해서, 직접 Dockerfile로 이미지를 빌드해 웹 서버 컨테이너를 띄워보고, 마지막으로 컨테이너가 지워져도 데이터가 남도록 하는 두 가지 방법(호스트 디렉토리를 그대로 연결하는 bind mount, 도커가 별도로 관리하는 named volume)을 비교해보는 순서로 진행한다.

아래 표는 이 글에서 실습한 명령어를 정리한 것이다.

명령어	하는 동작	실습에서 확인한 것
docker info	현재 도커 클라이언트·서버(데몬)의 상태 확인	CLI가 PATH에 없을 땐 command not found, CLI는 있는데 데몬만 꺼져 있으면 Client는 정상 출력되고 Server만 연결 에러 — 서로 다른 두 실패가 다른 메시지로 구분되는 것
docker pull	이미지를 레지스트리(Docker Hub)에서 로컬로 받아오기만 함	pull 직후엔 docker images에 이미지만 잡히고, 컨테이너는 그 뒤 create를 실행해야 비로소 docker ps -a에 나타나는 것
docker run	이미지로 새 컨테이너를 만들고 곧바로 실행	로컬에 이미지가 없으면 알아서 pull까지 해주는 것, -it(대화형)·-dit(백그라운드+대화형)·-p(포트 매핑)·-v(볼륨 연결) 옵션 조합에 따라 컨테이너가 각각 다르게 동작하는 것
docker images	로컬에 받아둔 이미지 목록 확인	pull·build·rmi를 할 때마다 목록에 이미지가 생기고 지워지는 걸 그때그때 대조한 것
docker ps / docker ps -a	실행 중인 / (정지된 것까지 포함한) 전체 컨테이너 목록 확인	컨테이너마다 Created·Up·Exited 각 상태가 STATUS 칼럼에 어떻게 나타나는지 실습 곳곳에서 확인한 것
docker create	컨테이너를 만들기만 하고 실행하지는 않음	docker ps -a에 STATUS가 곧바로 Created로만 잡히고, start를 해야 비로소 실행된다는 것
docker start	만들어져 있는(멈춘) 컨테이너를 실행	start했을 때 화면엔 컨테이너 이름만 찍히고, hello-world 특성상 곧바로 다시 Exited로 돌아가는 것
docker exec	이미 떠 있는 컨테이너 안에서 새 프로세스(bash 등)를 추가로 실행	exec로 들어간 bash에서 exit해도 컨테이너의 메인 프로세스는 그대로 살아있어서 docker ps -a에 계속 Up으로 남는 것
docker attach	컨테이너의 메인 프로세스(PID 1)에 직접 연결	attach 상태에서 exit하면 이번엔 메인 프로세스 자체가 끝나버려서 컨테이너가 Exited로 바뀌는 것 — exec와 정반대 결과
docker rm / docker rmi	컨테이너 삭제 / 이미지 삭제	이미지를 쓰고 있는 컨테이너가 남아있으면 rmi가 거부되고, 그 컨테이너를 먼저 rm해야 rmi가 되는 순서를 에러 메시지로 직접 본 것
docker build	Dockerfile을 읽어서 새 이미지를 생성	FROM nginx:alpine에 COPY로 정적 파일 한 장을 얹은 my-web:1.0 이미지를 실제로 빌드하고, 그 이미지로 컨테이너를 띄워 curl로 응답을 확인한 것
docker logs	컨테이너의 출력 로그 확인	nginx 부팅 로그 사이에, 앞서 curl로 보낸 요청이 접속 기록으로 그대로 남아있는 것
docker stats	실행 중인 컨테이너의 CPU·메모리 등 리소스 사용량 확인	동시에 떠 있는 두 컨테이너의 리소스 사용량이 한 화면에서 각각 독립적으로 잡히는 것
docker volume create / -v	이름 붙은 볼륨을 생성 / 컨테이너에 볼륨이나 호스트 디렉토리를 연결	호스트 디렉토리를 그대로 연결한 bind mount는 컨테이너 안팎에서 같은 파일을 실시간으로 주고받고, named volume은 컨테이너를 지운 뒤 새 컨테이너에 같은 볼륨을 다시 연결해도 데이터가 그대로 남아있는 것
도커가 실제로 설치·실행되고 있는지부터 확인한다. 처음 docker info를 실행하면 command not found로 실패하는데, 이건 도커 데몬이 잠깐 꺼져 있어서가 아니라 이 컴퓨터에서 docker 명령어 자체가 PATH에 아직 한 번도 연결된 적이 없었기 때문이다. OrbStack을 처음 켜면서 CLI가 PATH에 연결된 뒤로는 같은 명령이 클라이언트·서버 버전, 사용 중인 스토리지 드라이버, 컨테이너·이미지 개수 같은 정보를 정상적으로 출력한다. 세 번째 docker info 결과는 앞의 두 경우와 또 다른데, OrbStack을 다시 꺼둔 상태에서 실행한 것이라 이번엔 command not found는 아니지만 Client 항목(CLI 자체 정보)만 정상 출력되고 Server 항목은 Cannot connect to the Docker daemon ... Is the docker daemon running?으로 실패한다. 즉 CLI가 PATH에 없는 것과 데몬이 꺼져 있는 것은 서로 다른 실패 상태이고, 각각 다른 에러 메시지로 구분된다.

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % docker info
zsh: command not found: docker

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % docker info
Client:
 Version:    28.5.2
 Context:    orbstack
 Debug Mode: false
 Plugins:
  buildx: Docker Buildx (Docker Inc.)
    Version:  v0.29.1
    Path:     /Users/qwera19976266/.docker/cli-plugins/docker-buildx
  compose: Docker Compose (Docker Inc.)
    Version:  v2.40.3
    Path:     /Users/qwera19976266/.docker/cli-plugins/docker-compose

Server:
 Containers: 0
  Running: 0
  Paused: 0
  Stopped: 0
 Images: 0
 Server Version: 28.5.2
 Storage Driver: overlay2
  Backing Filesystem: btrfs
  Supports d_type: true
  Using metacopy: false
  Native Overlay Diff: true
  userxattr: false
 Logging Driver: json-file
 Cgroup Driver: cgroupfs
 Cgroup Version: 2
 Plugins:
  Volume: local
  Network: bridge host ipvlan macvlan null overlay
  Log: awslogs fluentd gcplogs gelf journald json-file local splunk syslog
 CDI spec directories:
  /etc/cdi
  /var/run/cdi
 Swarm: inactive
 Runtimes: io.containerd.runc.v2 runc
 Default Runtime: runc
 Init Binary: docker-init
 containerd version: 1c4457e00facac03ce1d75f7b6777a7a851e5c41
 runc version: d842d7719497cc3b774fd71620278ac9e17710e0
 init version: de40ad0
 Security Options:
  seccomp
   Profile: builtin
  cgroupns
 Kernel Version: 6.17.8-orbstack-00308-g8f9c941121b1
 Operating System: OrbStack
 OSType: linux
 Architecture: x86_64
 CPUs: 6
 Total Memory: 15.67GiB
 Name: orbstack
 ID: db9c2f92-ee24-4863-8b94-43973549520f
 Docker Root Dir: /var/lib/docker
 Debug Mode: false
 Experimental: false
 Insecure Registries:
  ::1/128
  127.0.0.0/8
 Live Restore Enabled: false
 Product License: Community Engine
 Default Address Pools:
   Base: 192.168.97.0/24, Size: 24
   Base: 192.168.107.0/24, Size: 24
   Base: 192.168.117.0/24, Size: 24
   Base: 192.168.147.0/24, Size: 24
   Base: 192.168.148.0/24, Size: 24
   Base: 192.168.155.0/24, Size: 24
   Base: 192.168.156.0/24, Size: 24
   Base: 192.168.158.0/24, Size: 24
   Base: 192.168.163.0/24, Size: 24
   Base: 192.168.164.0/24, Size: 24
   Base: 192.168.165.0/24, Size: 24
   Base: 192.168.166.0/24, Size: 24
   Base: 192.168.167.0/24, Size: 24
   Base: 192.168.171.0/24, Size: 24
   Base: 192.168.172.0/24, Size: 24
   Base: 192.168.181.0/24, Size: 24
   Base: 192.168.183.0/24, Size: 24
   Base: 192.168.186.0/24, Size: 24
   Base: 192.168.207.0/24, Size: 24
   Base: 192.168.214.0/24, Size: 24
   Base: 192.168.215.0/24, Size: 24
   Base: 192.168.216.0/24, Size: 24
   Base: 192.168.223.0/24, Size: 24
   Base: 192.168.227.0/24, Size: 24
   Base: 192.168.228.0/24, Size: 24
   Base: 192.168.229.0/24, Size: 24
   Base: 192.168.237.0/24, Size: 24
   Base: 192.168.239.0/24, Size: 24
   Base: 192.168.242.0/24, Size: 24
   Base: 192.168.247.0/24, Size: 24
   Base: fd07:b51a:cc66:d000::/56, Size: 64

WARNING: DOCKER_INSECURE_NO_IPTABLES_RAW is set

qwera19976266@c3r5s4 ~ % docker info
Client:
 Version:    28.5.2
 Context:    orbstack
 Debug Mode: false
 Plugins:
  buildx: Docker Buildx (Docker Inc.)
    Version:  v0.29.1
    Path:     /Users/qwera19976266/.docker/cli-plugins/docker-buildx
  compose: Docker Compose (Docker Inc.)
    Version:  v2.40.3
    Path:     /Users/qwera19976266/.docker/cli-plugins/docker-compose

Server:
Cannot connect to the Docker daemon at unix:///Users/qwera19976266/.orbstack/run/docker.sock. Is the docker daemon running?
docker run hello-world로 가장 기본적인 컨테이너를 실행해본다. 로컬에 hello-world 이미지가 없어서 도커가 먼저 Docker Hub에서 이미지를 pull한 뒤, 그 이미지로 컨테이너를 만들어 실행한다. hello-world 컨테이너는 안내 메시지를 한 번 출력하고 바로 끝나는 프로그램이라, docker images로 이미지가 받아진 걸 확인하고 docker ps(실행 중인 것만)에는 아무것도 안 잡히지만 docker ps -a(정지된 것까지 포함)에는 방금 실행하고 끝난 컨테이너(reverent_easley)가 Exited 상태로 남아있는 걸 볼 수 있다.

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
4f55086f7dd0: Pull complete
Digest: sha256:7f4da0fc94bcece205a8c0b6f4d11c8196924654ffe5c4d1aa439b7f632048b2
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % docker images
REPOSITORY    TAG       IMAGE ID       CREATED        SIZE
hello-world   latest    e2ac70e7319a   4 months ago   10.1kB

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % docker ps -a
CONTAINER ID   IMAGE         COMMAND    CREATED          STATUS                      PORTS     NAMES
4a44d16d6f92   hello-world   "/hello"   29 seconds ago   Exited (0) 29 seconds ago             reverent_easley
이미지를 지워본다. docker rmi로 방금 쓴 hello-world 이미지를 바로 지우려고 하면, 그 이미지로 만들어진 컨테이너(reverent_easley)가 아직 남아있어서 must be forced 에러로 거부된다. docker rm으로 그 컨테이너를 먼저 지운 뒤 docker ps -a로 컨테이너가 없어진 걸 확인하고, 다시 docker rmi를 실행하면 이번엔 이미지가 정상적으로 삭제되고 docker images에도 아무것도 남지 않는다. 즉 이미지는 그걸 쓰고 있는 컨테이너가 하나도 없어야 지울 수 있다.

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % docker images
REPOSITORY    TAG       IMAGE ID       CREATED        SIZE
hello-world   latest    e2ac70e7319a   4 months ago   10.1kB

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % docker ps -a
CONTAINER ID   IMAGE         COMMAND    CREATED         STATUS                     PORTS     NAMES
4a44d16d6f92   hello-world   "/hello"   4 minutes ago   Exited (0) 4 minutes ago             reverent_easley

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % docker rmi e2ac70e7319a
Error response from daemon: conflict: unable to delete e2ac70e7319a (must be forced) - image is being used by stopped container 4a44d16d6f92

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % docker rm 4a44d16d6f92
4a44d16d6f92

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % docker ps -a
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % docker rmi e2ac70e7319a
Untagged: hello-world:latest
Untagged: hello-world@sha256:7f4da0fc94bcece205a8c0b6f4d11c8196924654ffe5c4d1aa439b7f632048b2
Deleted: sha256:e2ac70e7319a02c5a477f5825259bd118b94e8b02c279c67afa63adab6d8685b
Deleted: sha256:897b3f2a7c1bc2f3d02432f7892fe31c6272c521ad4d70257df624504a3238b4

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % docker images
REPOSITORY   TAG       IMAGE ID   CREATED   SIZE
이번엔 docker pull hello-world로 이미지만 먼저 받아둔다. pull은 이미지를 내려받는 명령이라 컨테이너를 만들지는 않고, docker images로 이미지가 잡힌 것까지만 확인한다. 실제로 컨테이너가 생기는 건 바로 이어서 docker create --name hello1 hello-world를 실행하는 시점이다. 이렇게 만든 컨테이너는 docker ps -a에 상태가 곧바로 Created로 뜨는데, 이건 컨테이너 객체만 만들어졌을 뿐 아직 실행되지는 않았다는 뜻이다. docker start hello1로 실행하면 화면엔 컨테이너 이름만 찍히고, hello-world 특성상 할 일을 마치자마자 곧바로 끝나버려서 다시 docker ps -a를 보면 상태가 Exited로 바뀌어 있다.

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % docker pull hello-world
Using default tag: latest
latest: Pulling from library/hello-world
4f55086f7dd0: Pull complete
Digest: sha256:7f4da0fc94bcece205a8c0b6f4d11c8196924654ffe5c4d1aa439b7f632048b2
Status: Downloaded newer image for hello-world:latest
docker.io/library/hello-world:latest

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % docker images
REPOSITORY    TAG       IMAGE ID       CREATED        SIZE
hello-world   latest    e2ac70e7319a   4 months ago   10.1kB

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % docker create --name hello1 hello-world
9e330e85677c593b21aad46a033580e2634f5bb3e6a096f10c67cee1cebb65ee

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % docker ps -a
CONTAINER ID   IMAGE         COMMAND    CREATED         STATUS    PORTS     NAMES
9e330e85677c   hello-world   "/hello"   5 seconds ago   Created             hello1

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % docker start hello1
hello1

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % docker ps -a
CONTAINER ID   IMAGE         COMMAND    CREATED          STATUS                     PORTS     NAMES
9e330e85677c   hello-world   "/hello"   30 seconds ago   Exited (0) 3 seconds ago             hello1
이번엔 ubuntu 이미지로 직접 셸에 들어가본다. docker pull ubuntu로 이미지를 받은 뒤, docker run -it --name u1 ubuntu bash를 실행하면 컨테이너 안의 bash로 곧바로 진입한다(-i는 표준 입력을 열어두는 옵션, -t는 터미널을 붙여주는 옵션이다). 컨테이너 안에서 pwd·ls로 완전히 별개의 파일시스템에 들어와 있는 걸 확인하고, cat /etc/os-release로 이 컨테이너가 실제로 우분투(26.04 LTS)인 것도 확인한다. exit로 나오면 컨테이너의 메인 프로세스(bash)가 끝나버리기 때문에, docker ps -a에는 u1이 Exited 상태로 남는다.

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % docker pull ubuntu
Using default tag: latest
latest: Pulling from library/ubuntu
617772c7d19b: Pull complete
a7fb98a8eddd: Pull complete
Digest: sha256:678c6550cc43645e08669028bc177f50be4e7c5b8cca677067b1914d4afc7a03
Status: Downloaded newer image for ubuntu:latest
docker.io/library/ubuntu:latest

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % docker images
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
ubuntu       latest    86a1a31fdd84   11 days ago   100MB

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % docker run -it --name u1 ubuntu bash
root@8e2526c731e6:/# pwd
/
root@8e2526c731e6:/# ls
bin  boot  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
root@8e2526c731e6:/# cat /etc/os-release
PRETTY_NAME="Ubuntu 26.04 LTS"
NAME="Ubuntu"
VERSION_ID="26.04"
VERSION="26.04 LTS (Resolute Raccoon)"
VERSION_CODENAME=resolute
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=resolute
LOGO=ubuntu-logo
root@8e2526c731e6:/# exit
exit

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % docker ps -a
CONTAINER ID   IMAGE     COMMAND   CREATED              STATUS                     PORTS     NAMES
8e2526c731e6   ubuntu    "bash"    About a minute ago   Exited (0) 5 seconds ago             u1
이번엔 컨테이너를 백그라운드로 띄운 채 나중에 다시 접속해본다. docker run -dit --name u2 ubuntu bash는 -d(백그라운드)와 -it(대화형)를 같이 준 것으로, 컨테이너가 즉시 Up 상태로 뒤에서 계속 실행된다. docker exec -it u2 bash로 이미 떠 있는 이 컨테이너 안에 새 bash 프로세스를 하나 더 띄워서 들어가 보는데, ps aux로 보면 처음 컨테이너를 시작할 때 만들어진 bash(PID 1)와 방금 exec로 만든 bash가 같이 떠 있는 게 보인다. 여기서 exit로 나와도 컨테이너의 메인 프로세스(PID 1)는 그대로 살아있기 때문에 docker ps -a를 보면 u2는 계속 Up 상태다. 반면 docker attach u2는 exec처럼 새 프로세스를 만드는 게 아니라 그 메인 프로세스(PID 1) 자체에 연결하는 것이라, 여기서 exit하면 이번엔 메인 프로세스가 끝나버려서 컨테이너 자체가 Exited로 바뀐다. exec와 attach가 컨테이너 생명주기에 미치는 영향이 이렇게 다르다.

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % docker run -dit --name u2 ubuntu bash
5f1815e9424695c286235faf6cdd810ac811e0641e242016f96fbfdb2a77251f

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % docker ps -a
CONTAINER ID   IMAGE     COMMAND   CREATED         STATUS                          PORTS     NAMES
5f1815e94246   ubuntu    "bash"    5 seconds ago   Up 5 seconds                              u2
8e2526c731e6   ubuntu    "bash"    2 minutes ago   Exited (0) About a minute ago             u1

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % docker exec -it u2 bash
root@5f1815e94246:/# pwd
/
root@5f1815e94246:/# ls
bin  boot  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
root@5f1815e94246:/# ps aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.0   4776  3348 pts/0    Ss+  09:47   0:00 bash
root           8  0.1  0.0   4776  4172 pts/1    Ss   09:48   0:00 bash
root          16  0.0  0.0   6760  4096 pts/1    R+   09:49   0:00 ps aux
root@5f1815e94246:/# exit
exit

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % docker ps -a
CONTAINER ID   IMAGE     COMMAND   CREATED              STATUS                     PORTS     NAMES
5f1815e94246   ubuntu    "bash"    About a minute ago   Up About a minute                    u2
8e2526c731e6   ubuntu    "bash"    3 minutes ago        Exited (0) 2 minutes ago             u1

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % docker attach u2
root@5f1815e94246:/# pwd
/
root@5f1815e94246:/# ls
bin  boot  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
root@5f1815e94246:/# ps aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.0   4776  3332 pts/0    Ss   09:47   0:00 bash
root          18  0.0  0.0   6760  3920 pts/0    R+   09:49   0:00 ps aux
root@5f1815e94246:/# exit
exit

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % docker ps -a
CONTAINER ID   IMAGE     COMMAND   CREATED              STATUS                     PORTS     NAMES
5f1815e94246   ubuntu    "bash"    About a minute ago   Exited (0) 2 seconds ago             u2
8e2526c731e6   ubuntu    "bash"    3 minutes ago        Exited (0) 2 minutes ago             u1
이제 직접 이미지를 빌드해본다. mkdir -p docker-practice/site로 작업 디렉토리를 만들고, site/index.html에 Hello Codyssey라는 내용을 넣은 뒤, Dockerfile에 FROM nginx:alpine(nginx 웹서버 이미지를 베이스로 삼는다는 뜻)과 COPY site/ /usr/share/nginx/html/(방금 만든 정적 파일을 nginx의 기본 서빙 경로에 복사)을 적어둔다. docker build -t my-web:1.0 ./로 이 Dockerfile을 읽어서 my-web:1.0이라는 새 이미지를 만들고, docker run -d --name my-web-c -p 8080:80 my-web:1.0으로 그 이미지를 컨테이너로 띄우면서 컨테이너의 80번 포트를 호스트의 8080번 포트에 연결한다(-p 8080:80). curl localhost:8080으로 실제 호스트에서 접속해보면 index.html에 넣어둔 Hello Codyssey가 그대로 응답으로 돌아온다.

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % mkdir -p docker-practice/site

qwera19976266@c3r5s4 Codyssey-Pre-course-E1-1 % cd docker-practice

qwera19976266@c3r5s4 docker-practice % cat > site/index.html << 'EOF'
Hello Codyssey
EOF

qwera19976266@c3r5s4 docker-practice % cat > Dockerfile << 'EOF'
FROM nginx:alpine
COPY site/ /usr/share/nginx/html/
EOF

qwera19976266@c3r5s4 docker-practice % cat Dockerfile
FROM nginx:alpine
COPY site/ /usr/share/nginx/html/

qwera19976266@c3r5s4 docker-practice % cat site/index.html
Hello Codyssey

qwera19976266@c3r5s4 docker-practice % docker build -t my-web:1.0 ./
[+] Building 4.9s (7/7) FINISHED                                                                                                                                 docker:orbstack
 => [internal] load build definition from Dockerfile                                                                                                                        0.1s
 => => transferring dockerfile: 89B                                                                                                                                         0.0s
 => [internal] load metadata for docker.io/library/nginx:alpine                                                                                                             0.7s
 => [internal] load .dockerignore                                                                                                                                           0.2s
 => => transferring context: 2B                                                                                                                                             0.0s
 => [internal] load build context                                                                                                                                           0.2s
 => => transferring context: 85B                                                                                                                                            0.0s
 => [1/2] FROM docker.io/library/nginx:alpine@sha256:4a73073bd557c65b759505da037898b61f1be6cbcc3c2c3aeac22d2a470c1752                                                       3.0s
 => => resolve docker.io/library/nginx:alpine@sha256:4a73073bd557c65b759505da037898b61f1be6cbcc3c2c3aeac22d2a470c1752                                                       0.2s
 => => sha256:4a73073bd557c65b759505da037898b61f1be6cbcc3c2c3aeac22d2a470c1752 10.33kB / 10.33kB                                                                            0.0s
 => => sha256:1d40e3eb3bf4f138de1d67193f2aa5309fcaf343eb5ffadbf5e9439de1eb1ebb 2.50kB / 2.50kB                                                                              0.0s
 => => sha256:f0ba77f796e57c6fa89ae7f4fdad1665d6fcbd8e3f211535120542b337f9959e 12.32kB / 12.32kB                                                                            0.0s
 => => sha256:3cd534fe98c64d68a1f4f1c83abb8d5cba7ecfd7be88e592389929d12e6253da 1.89MB / 1.89MB                                                                              0.3s
 => => sha256:55afa1ecc21d2bb5e5045f32dafee56272ffd89860bac26f6c32123439af26a4 3.85MB / 3.85MB                                                                              0.7s
 => => sha256:1223f016b4e4a2c21f7c49d4837fbfd47a9da6436b511690ca1e582fc2810d59 627B / 627B                                                                                  0.4s
 => => sha256:62bec68d7c31c4c8a19d812d84da5f7748e54690c037979945b6c5b6c924b142 957B / 957B                                                                                  0.7s
 => => sha256:46f977ee452f4399c208714afa034868d6056864f8a0cf3c643ab143dd802c80 404B / 404B                                                                                  0.7s
 => => extracting sha256:55afa1ecc21d2bb5e5045f32dafee56272ffd89860bac26f6c32123439af26a4                                                                                   0.1s
 => => sha256:390dc935348d8070e695fbaae2a4bb114fb9e69c59f628e7576036ee9d5244c9 1.40kB / 1.40kB                                                                              0.9s
 => => sha256:46519e7231d2eb5604df229beb44d59719a489eaa7aca52982535a010b07a9ed 20.31MB / 20.31MB                                                                            1.4s
 => => sha256:d0008c891db48b5f526d914bce9e8d889fe1a9d1f08291ae03fe97f871726f38 1.21kB / 1.21kB                                                                              1.0s
 => => extracting sha256:3cd534fe98c64d68a1f4f1c83abb8d5cba7ecfd7be88e592389929d12e6253da                                                                                   0.1s
 => => extracting sha256:1223f016b4e4a2c21f7c49d4837fbfd47a9da6436b511690ca1e582fc2810d59                                                                                   0.0s
 => => extracting sha256:62bec68d7c31c4c8a19d812d84da5f7748e54690c037979945b6c5b6c924b142                                                                                   0.0s
 => => extracting sha256:46f977ee452f4399c208714afa034868d6056864f8a0cf3c643ab143dd802c80                                                                                   0.0s
 => => extracting sha256:d0008c891db48b5f526d914bce9e8d889fe1a9d1f08291ae03fe97f871726f38                                                                                   0.0s
 => => extracting sha256:390dc935348d8070e695fbaae2a4bb114fb9e69c59f628e7576036ee9d5244c9                                                                                   0.0s
 => => extracting sha256:46519e7231d2eb5604df229beb44d59719a489eaa7aca52982535a010b07a9ed                                                                                   0.4s
 => [2/2] COPY site/ /usr/share/nginx/html/                                                                                                                                 0.2s
 => exporting to image                                                                                                                                                      0.2s
 => => exporting layers                                                                                                                                                     0.2s
 => => writing image sha256:642bf0dd3e5e55da963ebff2e2d602382650b1ec70f09a919fba2784e4b599af                                                                                0.0s
 => => naming to docker.io/library/my-web:1.0                                                                                                                               0.0s

qwera19976266@c3r5s4 docker-practice % docker run -d --name my-web-c -p 8080:80 my-web:1.0
b24164a9f1998b0c3ab6567cae69c76bbd391e42e53ac44e93fc20fce62a8698

qwera19976266@c3r5s4 docker-practice % curl localhost:8080
Hello Codyssey

qwera19976266@c3r5s4 docker-practice % docker ps -a
CONTAINER ID   IMAGE        COMMAND                   CREATED              STATUS                      PORTS                                     NAMES
b24164a9f199   my-web:1.0   "/docker-entrypoint.…"   About a minute ago   Up About a minute           0.0.0.0:8080->80/tcp, [::]:8080->80/tcp   my-web-c
5f1815e94246   ubuntu       "bash"                    14 minutes ago       Exited (0) 12 minutes ago                                             u2
8e2526c731e6   ubuntu       "bash"                    16 minutes ago       Exited (0) 15 minutes ago                                             u1
포트를 하나 더 열어본다. 똑같이 -p 8080:80으로 my-web-c2를 띄우려고 하면, 8080번 포트는 이미 my-web-c가 쓰고 있어서 port is already allocated 에러가 난다. 흥미로운 건 컨테이너 자체는 만들어졌다는 점인데, docker ps -a를 보면 my-web-c2가 포트 바인딩에 실패해 시작되지 못한 채 Created 상태로 남아있다. 이번엔 -p 8082:80으로 포트를 바꿔서 my-web-c3를 띄우면 정상적으로 Up 상태가 되고, curl localhost:8082도 응답이 온다. 반면 매핑해준 적 없는 curl localhost:8081은 연결 자체가 거부되는데, 컨테이너의 80번 포트가 호스트의 특정 포트에 명시적으로 연결된 경우에만 호스트에서 접근할 수 있다는 걸 보여준다.

qwera19976266@c3r5s4 docker-practice % docker run -d --name my-web-c2 -p 8080:80 my-web:1.0
64c516892280c390334a60ae51747d8336b058209922982ba3a514b2b6238d05
docker: Error response from daemon: failed to set up container networking: driver failed programming external connectivity on endpoint my-web-c2 (f0bd168324d7569fa64e83fee1caa6fa44bdbe0596e7d430f540af95b13afa8d): Bind for 0.0.0.0:8080 failed: port is already allocated

Run 'docker run --help' for more information

qwera19976266@c3r5s4 docker-practice % docker ps -a
CONTAINER ID   IMAGE        COMMAND                   CREATED          STATUS                      PORTS                                     NAMES
64c516892280   my-web:1.0   "/docker-entrypoint.…"   9 seconds ago    Created                                                               my-web-c2
b24164a9f199   my-web:1.0   "/docker-entrypoint.…"   2 minutes ago    Up 2 minutes                0.0.0.0:8080->80/tcp, [::]:8080->80/tcp   my-web-c
5f1815e94246   ubuntu       "bash"                    15 minutes ago   Exited (0) 13 minutes ago                                             u2
8e2526c731e6   ubuntu       "bash"                    17 minutes ago   Exited (0) 16 minutes ago                                             u1

qwera19976266@c3r5s4 docker-practice % docker run -d --name my-web-c3 -p 8082:80 my-web:1.0
3db7b885113a8f0f54bd759b2775a98e2b9243daf41347ae719cd1c410c6ad08

qwera19976266@c3r5s4 docker-practice % docker ps -a
CONTAINER ID   IMAGE        COMMAND                   CREATED                  STATUS                      PORTS                                     NAMES
3db7b885113a   my-web:1.0   "/docker-entrypoint.…"   Less than a second ago   Up 3 seconds                0.0.0.0:8082->80/tcp, [::]:8082->80/tcp   my-web-c3
64c516892280   my-web:1.0   "/docker-entrypoint.…"   31 seconds ago           Created                                                               my-web-c2
b24164a9f199   my-web:1.0   "/docker-entrypoint.…"   2 minutes ago            Up 2 minutes                0.0.0.0:8080->80/tcp, [::]:8080->80/tcp   my-web-c
5f1815e94246   ubuntu       "bash"                    15 minutes ago           Exited (0) 13 minutes ago                                             u2
8e2526c731e6   ubuntu       "bash"                    17 minutes ago           Exited (0) 16 minutes ago                                             u1

qwera19976266@c3r5s4 docker-practice % curl localhost:8082
Hello Codyssey

qwera19976266@c3r5s4 docker-practice % curl localhost:8081
curl: (7) Failed to connect to localhost port 8081 after 0 ms: Couldn't connect to server
같은 결과를 브라우저로도 확인했다. localhost:8080과 localhost:8082는 매핑된 컨테이너가 응답해서 Hello Codyssey가 그대로 뜨고, 매핑해준 적 없는 localhost:8081은 브라우저에서도 ERR_CONNECTION_REFUSED로 접속이 거부된다.

브라우저에서 localhost:8080 접속 — Hello Codyssey 응답

브라우저에서 localhost:8081 접속 — 매핑되지 않은 포트라 연결 거부(ERR_CONNECTION_REFUSED)

브라우저에서 localhost:8082 접속 — Hello Codyssey 응답

docker logs my-web-c로 이 컨테이너의 출력을 확인하면 nginx가 켜지면서 남긴 부팅 로그 사이에, 아까 curl localhost:8080으로 보냈던 요청이 접속 로그(GET / HTTP/1.1 200)로 그대로 남아있는 걸 볼 수 있다. docker stats --no-stream으로는 지금 떠 있는 컨테이너들(my-web-c3, my-web-c)의 CPU·메모리 사용량을 한 번에 확인하는데, 둘 다 몇 MiB 수준의 가벼운 자원만 쓰고 있는 걸 볼 수 있다(--no-stream은 실시간 갱신 없이 한 번만 찍고 끝내는 옵션).

qwera19976266@c3r5s4 docker-practice % docker logs my-web-c
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
/docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
/docker-entrypoint.sh: Configuration complete; ready for start up
2026/08/05 10:00:43 [notice] 1#1: using the "epoll" event method
2026/08/05 10:00:43 [notice] 1#1: nginx/1.31.3
2026/08/05 10:00:43 [notice] 1#1: built by gcc 15.2.0 (Alpine 15.2.0)
2026/08/05 10:00:43 [notice] 1#1: OS: Linux 6.17.8-orbstack-00308-g8f9c941121b1
2026/08/05 10:00:43 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 20480:1048576
2026/08/05 10:00:43 [notice] 1#1: start worker processes
2026/08/05 10:00:43 [notice] 1#1: start worker process 30
2026/08/05 10:00:43 [notice] 1#1: start worker process 31
2026/08/05 10:00:43 [notice] 1#1: start worker process 32
2026/08/05 10:00:43 [notice] 1#1: start worker process 33
2026/08/05 10:00:43 [notice] 1#1: start worker process 34
2026/08/05 10:00:43 [notice] 1#1: start worker process 35
192.168.215.1 - - [05/Aug/2026:10:00:48 +0000] "GET / HTTP/1.1" 200 15 "-" "curl/8.7.1" "-"

qwera19976266@c3r5s4 docker-practice % docker stats --no-stream
CONTAINER ID   NAME        CPU %     MEM USAGE / LIMIT     MEM %     NET I/O         BLOCK I/O         PIDS
3db7b885113a   my-web-c3   0.00%     5.164MiB / 15.67GiB   0.03%     1.46kB / 798B   10.7MB / 8.19kB   7
b24164a9f199   my-web-c    0.00%     5.422MiB / 15.67GiB   0.03%     1.97kB / 798B   10.3MB / 8.19kB   7
이제 컨테이너가 지워져도 데이터가 남게 하는 방법을 실습한다. 먼저 호스트 쪽에 bind-test 디렉토리를 만들고 data.txt에 by host라는 내용을 써둔다. docker run -dit --name bind-c -v "$(pwd)/bind-test:/app" ubuntu로 컨테이너를 띄우는데, -v 호스트경로:컨테이너경로 형태로 지금 이 디렉토리의 bind-test를 컨테이너 안의 /app에 그대로 연결한다(bind mount). docker exec -it bind-c bash로 들어가서 /app/data.txt를 열어보면 호스트에서 써둔 by host가 그대로 보이고, 여기에 by container를 한 줄 더 추가한 뒤 컨테이너를 나와서 호스트 쪽 bind-test/data.txt를 다시 열어보면 컨테이너 안에서 추가한 줄까지 그대로 반영돼 있다. 호스트와 컨테이너가 사실상 같은 파일을 실시간으로 공유하고 있다는 뜻이다.

qwera19976266@c3r5s4 docker-practice % mkdir bind-test

qwera19976266@c3r5s4 docker-practice % echo "by host" > bind-test/data.txt

qwera19976266@c3r5s4 docker-practice % cat bind-test/data.txt
by host

qwera19976266@c3r5s4 docker-practice % docker run -dit --name bind-c -v "$(pwd)/bind-test:/app" ubuntu
80b3e699b4f62cdeda2c0b2fb382a8ffb365e17aa8c99c6905c1c5bdaeef2d4e

qwera19976266@c3r5s4 docker-practice % docker ps -a
CONTAINER ID   IMAGE        COMMAND                   CREATED          STATUS                      PORTS                                     NAMES
80b3e699b4f6   ubuntu       "/bin/bash"               2 seconds ago    Up 2 seconds                                                          bind-c
3db7b885113a   my-web:1.0   "/docker-entrypoint.…"   27 minutes ago   Up 27 minutes               0.0.0.0:8082->80/tcp, [::]:8082->80/tcp   my-web-c3
64c516892280   my-web:1.0   "/docker-entrypoint.…"   28 minutes ago   Created                                                               my-web-c2
b24164a9f199   my-web:1.0   "/docker-entrypoint.…"   30 minutes ago   Up 30 minutes               0.0.0.0:8080->80/tcp, [::]:8080->80/tcp   my-web-c
5f1815e94246   ubuntu       "bash"                    43 minutes ago   Exited (0) 41 minutes ago                                             u2
8e2526c731e6   ubuntu       "bash"                    45 minutes ago   Exited (0) 44 minutes ago                                             u1

qwera19976266@c3r5s4 docker-practice % docker exec -it bind-c bash
root@80b3e699b4f6:/# cat /app/data.txt
by host
root@80b3e699b4f6:/# echo "by container" >> /app/data.txt
root@80b3e699b4f6:/# cat /app/data.txt
by host
by container
root@80b3e699b4f6:/# exit
exit

qwera19976266@c3r5s4 docker-practice % cat bind-test/data.txt
by host
by container
이번엔 호스트 경로를 직접 지정하는 대신, 도커가 따로 관리하는 이름 붙은 저장 공간(named volume)을 써본다. docker volume create my-vol로 볼륨을 하나 만들고, docker run -dit --name vol-c -v my-vol:/app ubuntu로 이 볼륨을 컨테이너의 /app에 연결한다. 컨테이너 안에서 /app/data.txt에 by vol을 써넣은 뒤, find ~ -name "data.txt"로 호스트에서 관련 파일들의 실제 위치를 찾아보면 네 개의 경로가 나온다. 방금 bind mount로 연결했던 bind-test/data.txt, my-vol 볼륨의 실제 데이터가 저장된 ~/OrbStack/docker/volumes/my-vol/data.txt, 그리고 나머지 둘(~/OrbStack/docker/containers/vol-c/app/..., .../bind-c/app/...)은 OrbStack이 각 컨테이너의 마운트 상태를 호스트에서 들여다볼 수 있게 미러링해둔 경로다. 여기서 핵심은 다음 단계인데, docker rm -f vol-c로 이 컨테이너를 통째로 지운 뒤 docker run -dit --name vol-c2 -v my-vol:/app ubuntu로 같은 볼륨을 새 컨테이너에 다시 연결해서 cat /app/data.txt를 해보면 by vol이 그대로 남아있다. 컨테이너를 지워도 named volume에 담긴 데이터는 컨테이너의 생명주기와 별개로 남아있다는 걸 보여주는 실습이다.

qwera19976266@c3r5s4 docker-practice % docker volume create my-vol
my-vol

qwera19976266@c3r5s4 docker-practice % docker run -dit --name vol-c -v my-vol:/app ubuntu
30184695c5451cac0ba453e94aa56189b6e530f51174284fc75680acc4227991

qwera19976266@c3r5s4 docker-practice % docker ps -a
CONTAINER ID   IMAGE        COMMAND                   CREATED          STATUS                      PORTS                                     NAMES
30184695c545   ubuntu       "/bin/bash"               4 seconds ago    Up 3 seconds                                                          vol-c
80b3e699b4f6   ubuntu       "/bin/bash"               2 minutes ago    Up 2 minutes                                                          bind-c
3db7b885113a   my-web:1.0   "/docker-entrypoint.…"   30 minutes ago   Up 30 minutes               0.0.0.0:8082->80/tcp, [::]:8082->80/tcp   my-web-c3
64c516892280   my-web:1.0   "/docker-entrypoint.…"   30 minutes ago   Created                                                               my-web-c2
b24164a9f199   my-web:1.0   "/docker-entrypoint.…"   32 minutes ago   Up 32 minutes               0.0.0.0:8080->80/tcp, [::]:8080->80/tcp   my-web-c
5f1815e94246   ubuntu       "bash"                    45 minutes ago   Exited (0) 43 minutes ago                                             u2
8e2526c731e6   ubuntu       "bash"                    47 minutes ago   Exited (0) 46 minutes ago                                             u1

qwera19976266@c3r5s4 docker-practice % docker exec -it vol-c bash
root@30184695c545:/# echo "by vol" > /app/data.txt
root@30184695c545:/# cat /app/data.txt
by vol
root@30184695c545:/# exit
exit

qwera19976266@c3r5s4 docker-practice % find ~ -name "data.txt" 2>/dev/null
/Users/qwera19976266/OrbStack/docker/containers/vol-c/app/data.txt
/Users/qwera19976266/OrbStack/docker/containers/bind-c/app/data.txt
/Users/qwera19976266/OrbStack/docker/volumes/my-vol/data.txt
/Users/qwera19976266/Desktop/github/Codyssey-Pre-course-E1-1/docker-practice/bind-test/data.txt

qwera19976266@c3r5s4 docker-practice % docker rm -f vol-c
vol-c

qwera19976266@c3r5s4 docker-practice % docker ps -a
CONTAINER ID   IMAGE        COMMAND                   CREATED          STATUS                      PORTS                                     NAMES
80b3e699b4f6   ubuntu       "/bin/bash"               4 minutes ago    Up 4 minutes                                                          bind-c
3db7b885113a   my-web:1.0   "/docker-entrypoint.…"   32 minutes ago   Up 32 minutes               0.0.0.0:8082->80/tcp, [::]:8082->80/tcp   my-web-c3
64c516892280   my-web:1.0   "/docker-entrypoint.…"   33 minutes ago   Created                                                               my-web-c2
b24164a9f199   my-web:1.0   "/docker-entrypoint.…"   35 minutes ago   Up 35 minutes               0.0.0.0:8080->80/tcp, [::]:8080->80/tcp   my-web-c
5f1815e94246   ubuntu       "bash"                    48 minutes ago   Exited (0) 46 minutes ago                                             u2
8e2526c731e6   ubuntu       "bash"                    50 minutes ago   Exited (0) 49 minutes ago                                             u1

qwera19976266@c3r5s4 docker-practice % docker run -dit --name vol-c2 -v my-vol:/app ubuntu
5a47f87edbda922a95908e1b4fb47104fb13cd6ae303259be88c99d55f19f4f6

qwera19976266@c3r5s4 docker-practice % docker exec -it vol-c2 cat /app/data.txt
by vol
4. 트러블슈팅
1. SSH 키가 없어서 git clone 실패
문제: SSH 주소(git@github.com:...)로 git clone을 실행했더니 git@github.com: Permission denied (publickey).로 실패했다.
원인 가설: GitHub에게 "이 컴퓨터가 내 계정이 맞다"는 걸 증명할 SSH 키가 이 컴퓨터에 아직 없어서 인증 자체가 거부된 것으로 추정했다.
확인: ls -la ~/.ssh로 확인해보니 known_hosts(방금 git clone 과정에서 GitHub 서버를 처음 신뢰하며 자동 생성된 파일) 하나만 있고, 인증에 쓸 키 파일(id_ed25519 등)은 실제로 없었다.
해결: ssh-keygen -t ed25519 -C "test"로 새 키 쌍을 생성하고, cat id_ed25519.pub로 출력한 공개키를 GitHub의 SSH 설정 페이지(github.com/settings/keys)에 등록했다. 이후 같은 git clone 명령을 재시도하니 인증을 통과해 정상적으로 복제됐다.
2. docker info 첫 실행이 command not found로 실패
문제: 이 컴퓨터에서 처음 docker info를 실행했더니 zsh: command not found: docker로 실패했다.
원인 가설: 처음엔 OrbStack(도커 데몬)이 꺼져 있어서 실패한 것으로 짐작했다.
확인: OrbStack을 다시 꺼둔 상태에서 같은 명령을 재현해보니, 이번엔 command not found가 아니라 Client 섹션(CLI 자체 정보)은 정상 출력되고 Server 섹션만 Cannot connect to the Docker daemon ... Is the docker daemon running?으로 실패했다. 즉 데몬이 꺼져 있을 때 나는 에러는 command not found가 아니라 이 연결 에러였고, 앞서 세웠던 원인 가설은 틀렸다는 게 이 재현으로 드러났다. 처음의 command not found는 데몬 상태와 무관하게, 이 컴퓨터에서 docker 명령어 자체가 PATH에 아직 한 번도 연결된 적이 없었기 때문이었다.
해결: OrbStack을 처음 켜는 과정에서 CLI가 PATH에 연결된 뒤로는 docker info가 정상 동작했다. CLI가 PATH에 없는 것과 데몬이 꺼져 있는 것은 서로 다른 실패 상태이고, 각각 command not found와 Cannot connect to the Docker daemon ...이라는 다른 메시지로 구분된다는 걸 확인했다.