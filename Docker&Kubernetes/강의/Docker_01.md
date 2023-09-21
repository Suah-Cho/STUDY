# docker_01

생성일: 2023년 9월 20일 오전 9:05

**참고자료**

[이재홍의 언제나 최신 Docker](https://pyrasis.com/jHLsAlwaysUpToDateDocker)

[도커 무작정 따라하기](https://pyrasis.com/docker/2015/02/09/docker-for-dummies)

**도커 설치**

[Docker Desktop](https://docs.docker.com/desktop)

원 클릭 설치 애플리케이션

간단한 GUI를 제공

도커 데스크탑에 포함된 것

- [Docker Engine](https://docs.docker.com/engine/)
- **Docker CLI client**
- [Docker Buildx](https://docs.docker.com/build/)
- [Docker Extensions](https://docs.docker.com/desktop/extensions/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Docker Content Trust](https://docs.docker.com/engine/security/trust/)
- [Kubernetesopen_in](https://github.com/kubernetes/kubernetes/)
- [Credential Helper](https://github.com/docker/docker-credential-helpers/)

**주요 기능**

- 여러 언어 및 프레임 워크로 모든 클라우드 플랫폼에서 모든 `애플리케이션을 컨테이너화하고 공유할 수 있는 기능`
- 도커 개발 환경을 빠르게 설치하고 설정 가능
- 최신 버전의 쿠버네티스를 포함
- Hyper-V 가상화를 통한 빠르고 안정적인 성능 제공
- WSL2를 통해 Linux에서 기본적으로 작업 가능

**도커란?**

- 복잡한 리눅스 애플리케이션을 컨테이너로 묶어서 실행할 수 있다.
- 개발, 테스트, 서비스 환경을 하나로 통일하여 효율적으로 관리할 수 있다.
- 컨테이너(이미지)를 전 세계 사람들과 공유
    - 리눅스 커널에서 제공하는 컨테이너 기술을 이용

**컨테이너란?**

- 컨테이너는 가상화보다, 훨씬 가벼운 기술!

**가상 머신의 문제점**

![Untitled](docker01_1.png)

클라우스 서비스 : 가상화 기술을 이용하여 서버를 임대해주는 서비스

**도커의 특징**

- 게스트 os를 설치하지 않는다.
- 하드웨어 가상화 계층이 없다.
- 이미지 생성과 배포에 특화
- 이미지 버전 관리도 제공하며 중앙 저장소에 이미지를 올리고 받을 수 있다.(push/pull)
- github와 비슷한 형태로 도커 이미지를 공유하는 Docker Hub제공(GitHub처럼 유료 저장소도 제공)
- 다양한 API를 제공하여 원하는 만큼 자동화 가능
    - 개발과 서버 운영에 매우 우용하다.

**도커 이미지와 컨테이너**

- 도커 이미지
    - 저장소에 올리고 받는 것(push, pull)
    - 서비스 운영에 필요한 서버 프로그램, 소스 코드, 컴파일된 실행 파일을 묶은 형태
- 컨테이너
    - 이미지를 실행한 상태
    - 이미지로 여러 개의 컨테이너를 만들 수 있다.

⇒ 이미지 : 실행 파일 , 컨테이너 : 프로세스

**도커의 이미지 처리 방식**

- 유니온 파일 시스템 형식(aufs, btrfs, devicemapper)
    
    ![Untitled](docker01_2.png)
    
    ![Untitled](docker01_3.png)
    
- 각 이미지는 의존 관계를 형성한다.
    
    ![Untitled](docker01_4.png)
    

**클라우드 환경**

- 가상화가 발전하면서 클라우드 환경으로 변화
- 가상 서버를 임대하여 사용한 만큼만 요금 지불
- 클릭 몇번만으로 가상 서버를 생성 + 추가 + 삭제 가능
- 서버 대수가 많아지면서 사람이 일일이 세팅하기 힘들어짐

**Immutable Infrastructure**

- 호스트 OS와 서비스 운영 환경(서버 프로그램, 소스 코드, 컴파일 된 바이너리)을 분리
- 한 번 설정한 운영 환경은 변경하지 않는다(Immutable)는 개념
- 서비스 운영 환경을 이미지로 생성한 뒤 서버에 배포하여 실행
- 서비스가 없데이트되면 운영 환경 자체를 변경하지 않고, 이미지를 새로 생성하여 배포
- 클라우드 플랫폼에서 서버를 쓰고 버리는 것과 같이 Immutable Infrastructure도 서비스 운영 환경 이미지를 한번 쓰고 버림
- 장점
    - 편리한 관리
        - 서비스 환경 이미지만 관리하면 됨
        - 중앙 관리를 통한 체계적인 배포와 관리
        - 이미지 생성에 버전 관리 시스템 활용
    - 확장
        - 이미지 하나로 서버를 계속 찍어낼 수 있음
        - 클라우드 플랫폼의 자동 확장(Auto Scaling) 기능과 연동하여 손쉽게 서비스 확장
    - 테스트
        - 개발자 PC, 테스트 서버에서 이미지를 실행만 하면 서비스 운영 환경과 동일한 환경이 구성됨
        - 테스크가 간편
    - 가볍다
        - 운영체제와 서비스 환경을 분리하여 가볍고 어디서든 실행 가능한 환경 제공
- 도커는 Immutable Infrastructure를 구현한 프로젝트

**도커의 생명 주기**

- Build
- Ship
- Run

**도커 구성 요소**

![[https://docs.docker.com/get-started/overview/#docker-architecture](https://docs.docker.com/get-started/overview/#docker-architecture)](docker_01%20175bcf43ea934c2c94aaef17fece9dc4/Untitled%204.png)

[https://docs.docker.com/get-started/overview/#docker-architecture](https://docs.docker.com/get-started/overview/#docker-architecture)

- **Docker Daemon**
    - dockerd
    - 도커 API 요청을 수신
    - 도커 이미지, 컨테이너, 네트워크, 볼륨과 같은 도커 객체를 관리
    - 도커 서비스를 관리하기 위해 다른 데몬과 통신
    
- **Client**
    - docker
    - 도커 사용자가 도커와 상호작용하는 기본 방법
    - 도커 사용자의 명령을 도커 API를 사용해서 도커 데몬으로 전달
    - 하나 이상의 도커 데콘과 통신이 가능

- **Registry**
    - 도커 이미지 저장소
    - 도커 이미지를 저장하고 배포하는 표준 방법
    - 퍼블릭 저장소와 프라이빗 저장소
        - 퍼블릭 저장소
            - 별도로 지정하지 않으면 기본값으로 Docker Hub을 사용
                
                [Docker Hub 회원가입](https://hub.docker.com/)
                
    

**도커 객체(Docker Objects)**

- 이미지
    - 컨테이너를 생성할 때 필요한 요소(가상머신을 생성할 때 사용하는 가상머신 이미지 또는 ISO파일과 비슷한 개념)
    - 여러 개의 계층으로 된 바이너리 파일로 존재
    - 컨테이너를 생성하고 실행할 때 읽기 전용으로 사용됨
    - 저장소(registy)/리포지토리(repository):태그(tag)
    
- 컨테이너
    - 도커 이미지로 생성한 해당 이미지의 목적에 맞는 파일이 들어있는 파일 시스템과 격리된 시스템 자원 및 네트워크를 사용할 수 있는 독립된 공간
    - 컨테이너는 이미지를 읽기 전용으로 사용하되 이미지에서 변경된 사항만 컨테이너 계층에 저장하므로 컨테이너에서 무엇을 하든지 원래 이미지는 영향을 받지 않는다.
    - 생성된 컨테이너는 각기 독립된 파일 시스템을 제공받으며 호스와 분리되어 있으므로 특정 컨테이너에서 어떤 애플리케이션을 설치하거나 삭제해도 다른 컨테이너와 호스트는 변화가 없음

**도커 컨테이너 라이프사이클**

![Untitled](docker01_6.png)

![Untitled](docker01_7.png)
