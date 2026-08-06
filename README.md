# Codyssey Custom Docker Image

## 1. 프로젝트 개요(미션 목표 요약)

- 선택: (B) Linux 베이스 이미지 + 기능 추가
- 베이스: ubuntu:24.04
- 설치 패키지: python3, curl
- 사용자: codyssey
- 환경 변수: APP_PORT, APP_MESSAGE
- Docker HEALTHCHECK 추가

## 2. 실행 환경(OS/쉘/터미널, Docker 버전, Git 버전)


## 3. 수행 항목 체크리스트(터미널/권한/Docker/Dockerfile/포트/Git/GitHub)

1. docker build -t codyssey-custom:latest .
2. docker run --rm -p 8080:8080 codyssey-custom:latest
3. curl http://localhost:8080

## 4. 검증 방법(어떤 명령으로 무엇을 확인했는지) + 결과 위치 링크

- docker build 성공
- curl 응답 200 OK
- HEALTHCHECK 정상

## 5. 트러블슈팅 2건 이상(문제 → 원인 가설 → 확인 → 해결/대안)


<!-- 기술 문서만 읽어도 전체 수행 내용을 파악할 수 있어야 한다. -->