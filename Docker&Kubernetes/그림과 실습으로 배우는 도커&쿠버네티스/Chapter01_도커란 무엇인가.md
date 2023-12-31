
## Chapter 1
### 1. 도커란 무엇인가?
### 도커란?
- `데이터 또는 프로그램을 격리시는 기능`을 제공하는 소프트웨어
- 다양한 프로그램과 데이터를 각각 독립된 환경에 격리하는 기능 제공

### 컨테이너와 도커 엔진
- 컨테이너
    - 독립된 창고에 데이터나 프로그램을 두는 것
- 도커(Docker)
    - 컨테이너를 다루는 기능을 제공하는 소프트웨어
- 도커 엔진
    - 컨테이너 생성 및 구동 가능

### 컨테이너
#### 이미지 + 도커 엔진 => 컨테이너
**이미지란?**
- 베이스 이미지
    - 리눅스 배포판의 유저래드만 설치된 파일
    - 보통 리눅스 배포판 이름으로 되어 있다.
    - `베이스 이비지에 필요한 프로그램과 라이브러리, 소스를 설치한 뒤 파일 하나로 만든 것`
- Docker은 이미지를 통째로 생성하지 않고, 바뀐 부분만 생성한 뒤 부모 이미지를 계속 `참조`하는 방식으로 동작한다. => `레이어`

**컨테이너**
- 이미지를 실행한 상태
- 하나의 이미지로 여러 개의 컨테이너 만들 수 있다.
    - 운영체제로 보면 이미지는 실행파일이고 컨테이너는 프로세스
- 이미 실행된 컨테이너에서 변경된 부분을 이미지로 생성 가능

**도커에서는 리눅스만 이용한다?**
- 도커는 Linux 운영체제가 필요하다.
- 윈도우나 macOS에서 도커를 구동하려면 내부적으로 리눅스가 사용된다.

### 데이터나 프로그램을 독립된 환경에 격리해야하는 이유

대부분 프로그램은 프로그램 단독으로 동작하는 것이 아니라 어떤 실행 환경이나 라이브러리, 다른 프로그램을 이용해 동작한다.  
 
프로그램 하나를 업데이트 한다면?  
=> 다른 프로그램에도 영향을 미친다.
`대부분의 문제는 프로그램 간 공유`에 있다.

**프로그램 격리란?**
컨테이너 안에 들어있는 프로그램은 다른 프로그램과 격리된 상태가 된다.  
=> 도커 컨테이너는 완전히 독립된 환경이므로 여러 컨테이너에서 같은 프로그램을실행할 수 있다. (버전이 완전히 동일해도 상관 X)


### 2.서버와 도커
### 서버
- 서버 : 어떤 서비스(service)를 제공(serve)하는 것
    - 기능적 의미의 서버
    - 물리적 컴퓨터로서의 서버

- 서버의 기능은 소프트웨어가 제공하는 것으로, 소프트웨어를 설치하면 `서버`의 기능을 가지게 된다.  
예) 웹 서버, 메일 서버, 데이터베이스 서버, 파일 서버, DNS 서버, DHCP 서버, FTP 서버, 프락시 서버, 인증 서버

- 서버의 운영체제로는 주로 리눅스가 사용된다.

## 서버와 도커
- 컨테이너 기술을 활용하면 여러 개의 웹 서버를 올릴 수 있다.
    - 여러 개의 물리적 서버로 나누웠던 서버를 하나의 물리 서버에 컨테이너로 나누어 올리면 프로젝트 비용을 감소시킬 수 있다.
- 컨테이너를 쉽고 자유롭게 옮길 수 있다.
    - 실제로 컨테이너 자체를 옮기는 것은 아니다.

        (컨테이너 정보를 내보내기한 다음, 다른 도커 엔진에서 복원하는 형태) 

    => 똑같은 상태로 튜닝한 컨테이너를 팀원 전원에게 배포해 모두가 동일한 개발환경을 사용할 수 있다.
    - 도커를 이용하면 물리적 환경의 차이, 서버 구성의 차이를 무시할 수 있어 `운영 서버와 개발 서버의 환경 차이로 인한 문제`를 원천적으로 방지할 수 있다.
