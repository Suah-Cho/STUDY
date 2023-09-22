# docker_03

생성일: 2023년 9월 20일 오전 9:05

### Dockerfile 작성 시 유의 사항 1 - 사용자 입력이 발생하지 않도록 하고, 포그라운드 프로세스로 실행되도록 해야 한다.

**우분투 컨테이너에 아파치 웹 서버를 설치하고 hello.html파일을 /var/www/html 디렉터리에 추가**

c:\docker\webserver

```powershell
docker container run --rm -it -p 8080:80 ubuntu
root@177b0a6a50e5:/#
root@177b0a6a50e5:/# apt-get update

root@177b0a6a50e5:/# apt-get install apache2
root@177b0a6a50e5:/# apachectl start
AH00558: apache2: Could not reliably determine the server's fully qualified domain name, using 172.17.0.2. Set the 'ServerName' directive globally to suppress this message

root@177b0a6a50e5:/# ls /var/www/html/
index.html
root@177b0a6a50e5:/# ctrl + p + q

docker container ls
CONTAINER ID   IMAGE     COMMAND       CREATED         STATUS         PORTS                  NAMES
177b0a6a50e5   ubuntu    "/bin/bash"   6 minutes ago   Up 6 minutes   0.0.0.0:8080->80/tcp   pedantic_noether
```

hello.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h1>Hello, Docker!!!</h1>
</body>
</html>
```

```html
docker container cp .\hello.html 177b0a6a50e5:/var/www/html/
Successfully copied 2.05kB to 177b0a6a50e5:/var/www/html/

docker container exec 177b0a6a50e5 cat /var/www/html/hello.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h1>Hello, Docker!!!</h1>
</body>
</html>
```

**동일한 기능을 제공하도록 Dockerfile을 작성해 컨테이너 이미지를 생성**

Dockerfile

```docker
FROM ubuntu
ENV  DEBIAN_FRONTEND=noninteractive
RUN  apt-get update
RUN  apt-get install apache2
ADD  hello.html /var/www/html/
CMD  apachectl start
```

```powershell
docker image build -t myimage:0.0 .

docker image ls
REPOSITORY   TAG       IMAGE ID       CREATED         SIZE
myimage      0.0       8c846cc8cd85   8 seconds ago   230MB
ubuntu       latest    c6b84b685f35   5 weeks ago     77.8MB

docker container run -p 8888:80 myimage:0.0
AH00558: apache2: Could not reliably determine the server's fully qualified domain name, using 172.17.0.3. Set the 'ServerName' directive globally to suppress this message

docker container ls -a
CONTAINER ID   IMAGE         COMMAND                   CREATED          STATUS                      PORTS                  NAMES
3f7ba55d9ab9   myimage:0.0   "/bin/sh -c 'apachec…"   26 seconds ago   Exited (0) 24 seconds ago                          nervous_boyd
177b0a6a50e5   ubuntu        "/bin/bash"               31 minutes ago   Up 31 minutes               0.0.0.0:8080->80/tcp   pedantic_noether
```

Dockerfile 수정

```docker
FROM ubuntu
ENV  DEBIAN_FRONTEND=noninteractive
RUN  apt-get update
RUN  apt-get install apache2 -y
ADD  hello.html /var/www/html/
CMD  apachectl -DFOREGROUND
```

```powershell
docker image build -t myimage:0.0 .

docker image ls
REPOSITORY   TAG       IMAGE ID       CREATED         SIZE
<none>       <none>    8c846cc8cd85   6 minutes ago   230MB
myimage      0.0       ef683b504e29   6 minutes ago   230MB
ubuntu       latest    c6b84b685f35   5 weeks ago     77.8MB

docker container run -p 8888:80 myimage:0.0
AH00558: apache2: Could not reliably determine the server's fully qualified domain name, using 172.17.0.3. Set the 'ServerName' directive globally to suppress this message
```

**컨테이너 내부에서 hello2.html파일을 추가하도록 Dockerfile을 수정**

```docker
FROM ubuntu
ENV  DEBIAN_FRONTEND=noninteractive
RUN  apt-get update
RUN  apt-get install apache2 -y
ADD  hello.html /var/www/html/
WORKDIR /var/www/html
RUN     ["/bin/bash", "-c", "echo hello2 >> hello2.html"]
EXPOSE  80
CMD  apachectl -DFOREGROUND
```

**이미지 빌드 후 컨테이너 실행**

```powershell
docker image build -t myimage:1.0 .

docker image ls
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
myimage      1.0       60db53cc6e55   14 seconds ago   230MB
myimage      0.0       ef683b504e29   49 minutes ago   230MB
<none>       <none>    8c846cc8cd85   49 minutes ago   230MB
ubuntu       latest    c6b84b685f35   5 weeks ago      77.8MB

docker container run -p 8888:80 -it myimage:1.0
AH00558: apache2: Could not reliably determine the server's fully qualified domain name, using 172.17.0.3. Set the 'ServerName' directive globally to suppress this message
ctlr + p + q

docker container ls
CONTAINER ID   IMAGE         COMMAND                   CREATED             STATUS             PORTS                  NAMES
fcf134ed931b   myimage:1.0   "/bin/sh -c 'apachec…"   45 seconds ago      Up 44 seconds      0.0.0.0:8888->80/tcp   hardcore_lamarr
177b0a6a50e5   ubuntu        "/bin/bash"               About an hour ago   Up About an hour   0.0.0.0:8080->80/tcp   pedantic_noether
```

**RUN, CMD, ENTRYPOINT에서 명령어를 기술하는 방법**

JSON 배열 형식은 쉘을 실행하거나 어떤 종류의 확장도 수행하지 않고 직접 해석

```docker
CMD command_string
CMD [ "/bin/sh", "-c", "command_string" ]

CMD mkdir /echo		⇒ /bin/sh -c mkdir /echo 형식으로 실행
CMD [ "mkdir", "/echo" ] 	⇒ mkdir /echo 형식으로 실행
```

**COPY, ADD**

- COPY는 로컬의 파일만 이미지에 추가할 수 있지만, ADD는 외부 URL 및 tar 파일에서도 파일을 추가할 수 있음 (tar파일의 경우 자동으로 해제해서 추가)
- ADD 보다는 **COPY 권장**(의도하지 않은 파일 추가를 방지)

**WORKDIR**

- 작업 디렉터리를 지정

```powershell
docker container exec -it fcf134ed931b /bin/bash
root@fcf134ed931b:/var/www/html#
```

**EXPOSE**

- 이미지에서 노출할 포트를 설정

```powershell
docker container run -P -it myimage:1.0
// -P == -p
AH00558: apache2: Could not reliably determine the server's fully qualified domain name, using 172.17.0.4. Set the 'ServerName' directive globally to suppress this message
ctrl + p + q

docker container ls
CONTAINER ID   IMAGE         COMMAND                   CREATED          STATUS          PORTS                   NAMES
7f237ae45a4c   myimage:1.0   "/bin/sh -c 'apachec…"   14 seconds ago   Up 13 seconds   0.0.0.0:32768->80/tcp   serene_cray
fcf134ed931b   myimage:1.0   "/bin/sh -c 'apachec…"   15 minutes ago   Up 15 minutes   0.0.0.0:8888->80/tcp    hardcore_lamarr
177b0a6a50e5   ubuntu        "/bin/bash"               2 hours ago      Up 2 hours      0.0.0.0:8080->80/tcp    pedantic_noether
```

**CMD vs ENTRYPOINT**

- entrypoint가 설정되지 않았다면 cmd에 설정된 명령어를 그대로 실행하지만, entrypoint가 설정되었다면 cmd는 단지 entrypoint에 대한 인자의 기능을 수행

Dockerfile_cmd

```docker
FROM ubuntu
CMD ["echo", "hello"]
```

```bash
docker image build -f Dockerfile_cmd -t cmding .
[+] Building 0.1s (5/5) FINISHED                                           docker:default
 => [internal] load build definition from Dockerfile_cmd                             0.0s
 => => transferring dockerfile: 68B                                                  0.0s
 => [internal] load .dockerignore                                                    0.0s
 => => transferring context: 2B                                                      0.0s
 => [internal] load metadata for docker.io/library/ubuntu:latest                     0.0s
 => CACHED [1/1] FROM docker.io/library/ubuntu                                       0.0s
 => exporting to image                                                               0.0s
 => => exporting layers                                                              0.0s
 => => writing image sha256:db9fbba8bfa00b4d770c60df2bbeda1e746cc05d740f6f0131996c0  0.0s
 => => naming to docker.io/library/cmdimg                                            0.0s

docker image ls
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
myimage      1.0       a37a95f7eb3e   33 minutes ago   230MB
myimage      0.0       856fddef1368   37 minutes ago   230MB
<none>       <none>    d563229c90c7   37 minutes ago   230MB
cmdimg       latest    db9fbba8bfa0   5 weeks ago      77.8MB
ubuntu       latest    c6b84b685f35   5 weeks ago      77.8MB

docker container run --rm cmdimg
hello
```

Dockerfile_entrypoint

```docker
FROM ubuntu
ENTRYPOINT ["echo", "hello"]
```

```bash
docker image build -f Dockerfile_entrypoint -t entrypointimg .
[+] Building 0.0s (5/5) FINISHED                                           docker:default
 => [internal] load .dockerignore                                                    0.0s
 => => transferring context: 2B                                                      0.0s
 => [internal] load build definition from Dockerfile_entrypoint                      0.0s
 => => transferring dockerfile: 75B                                                  0.0s
 => [internal] load metadata for docker.io/library/ubuntu:latest                     0.0s
 => CACHED [1/1] FROM docker.io/library/ubuntu                                       0.0s
 => exporting to image                                                               0.0s
 => => exporting layers                                                              0.0s
 => => writing image sha256:db9fbba8bfa00b4d770c60df2bbeda1e746cc05d740f6f0131996c0  0.0s
 => => naming to docker.io/library/entrypointimg                                     0.0s

docker container run entrypointimg
hello

docker container run entrypointimg echo world
hello echo world

// /bin/sh -c echo hello echo world 형식으로 실행
// echo라는 명렁어에 world가 파라미터로 전달된 것

docker container run --entrypoint="echo" entrypointimg world
world

// --entrypoint -> 명령어만 넣을 수 있다.
// 뒤에 echo 명렁어의 파라미터값을 넣어주는 것이다.
```

![Untitled](docker03/docker03_1.png)

entrypoint는 컨테이너가 올라갈 때 명령어를 보호하고 싶을 때 혹은 반드시 이 명령어로 실행하고 싶을 때 사용한다.

### Dockerfile 작성 시 유의사항 2 - 도커 이미지 크기가 커지지 않도록 유의

- 도커 컨테이너 이미지를 빌드하고 배포하는 시간을 단축하기 위해서는 도커 이미지 크기를 최대한 작게 유지하는 것이 좋다.
- Dockerfile의 모든 명령어는 레이어를 생성하고, 생성된 레이어는 저장
- 실제 컨테이너에서 사용하지 않는 (혹은 못 하는) 레이어도 저장 공간을 차지하게 되므로, 불필요한 레이어가 생성되지 않도록 하는 것이 중요하다.
- Dockerfile을 작성할 때 명령어를 묶어서 실행하는 것이 유익하다.
- 빌드 패턴 또는 다단계 도커 빌드 등을 이용해서 이미지를 작게 만드는 것이 필요하다.

1. **레이어 최소화**
    
    RUN 지시문을 결합해서 최적화 ⇒  Dockerfile의 각 줄은 도커 이미지에서 공간을 차지할 새 레이어를 생성하므로 가능한 한 지시문을 결합해서 적은 레이어를 생성
    

```powershell
docker container rm -f $(docker container ls -aq)
6618816bd5d8
74006590eeb1
f2867b028420
eb84cb05123a
d4baf67e53cf
d153985b0978
bbb92e898038
ab3dad07f18d
eb3a75d0cdec
fffcc04307c2
7ec15ece2049

docker image rm $(docker image ls -q)
Untagged: myimage:1.0
Deleted: sha256:a37a95f7eb3e2463fedebbb5ef9bc262aed04f175f7ef1b5e4f61a5e7540e6aa
Untagged: myimage:0.0
Deleted: sha256:856fddef1368d380d5fe4209ca352f48ce97fdf530cad35363688944d4e610af
Deleted: sha256:d563229c90c7e264f7e02ac4e438b910d93bc77afbed1375ab60edeaea8fced1
Untagged: cmdimg:latest
Deleted: sha256:db9fbba8bfa00b4d770c60df2bbeda1e746cc05d740f6f0131996c0170b61c97
Deleted: sha256:5f5ea37138b9f327d4715402c6cc78f993f52b3a5ae4037002f52ed399030158
Untagged: entrypointimg:latest
Deleted: sha256:5c4ce9e44b9531b1984949b7bdc7017956b196a9f50868c25f0b2a77e75822db
Untagged: ubuntu:latest
Untagged: ubuntu@sha256:aabed3296a3d45cede1dc866a24476c4d7e093aa806263c27ddaadbdce3c1054
Deleted: sha256:c6b84b685f35f1a5d63661f5d4aa662ad9b7ee4f4b8c394c022f25023c907b65
```

Dockerfile

```docker
FROM ubuntu
RUN mkdir /test
RUN fallocate -l 100m /test/dummy
RUN rm /test/dummy
```

```powershell
docker image build -t falloc_100m .
[+] Building 1.4s (8/8) FINISHED                                                     docker:default
 => [internal] load .dockerignore                                                              0.0s
 => => transferring context: 2B                                                                0.0s
 => [internal] load build definition from Dockerfile                                           0.0s
 => => transferring dockerfile: 120B                                                           0.0s
 => [internal] load metadata for docker.io/library/ubuntu:latest                               0.0s
 => [1/4] FROM docker.io/library/ubuntu                                                        0.0s
 => CACHED [2/4] RUN mkdir /test                                                               0.0s
 => [3/4] RUN fallocate -l 100m /test/dummy                                                    0.3s
 => [4/4] RUN rm /test/dummy                                                                   0.6s
 => exporting to image                                                                         0.4s
 => => exporting layers                                                                        0.4s
 => => writing image sha256:f2c36a7fbb44d5f4179cecc5bfd335daf2ec3b0b0606f0995c8a8d6d9a99af0d   0.0s
 => => naming to docker.io/library/falloc_100m                                                 0.0s

docker image pull ubuntu
Using default tag: latest
latest: Pulling from library/ubuntu
445a6a12be2b: Already exists
Digest: sha256:aabed3296a3d45cede1dc866a24476c4d7e093aa806263c27ddaadbdce3c1054
Status: Downloaded newer image for ubuntu:latest
docker.io/library/ubuntu:latest

docker image ls
REPOSITORY    TAG       IMAGE ID       CREATED          SIZE
falloc_100m   latest    f2c36a7fbb44   30 seconds ago   183MB
ubuntu        latest    c6b84b685f35   5 weeks ago      77.8MB

// 파일을 삭제했음에도 100m만큼 더 크다.
```

```docker
FROM ubuntu
RUN mkdir /test && fallocate -l 100m /test/dummy && rm /test/dummy
```

```powershell
docker image build -t falloc_100m .
[+] Building 0.4s (6/6) FINISHED                                                     docker:default
 => [internal] load .dockerignore                                                              0.0s
 => => transferring context: 2B                                                                0.0s
 => [internal] load build definition from Dockerfile                                           0.0s
 => => transferring dockerfile: 116B                                                           0.0s
 => [internal] load metadata for docker.io/library/ubuntu:latest                               0.0s
 => CACHED [1/2] FROM docker.io/library/ubuntu                                                 0.0s
 => [2/2] RUN mkdir /test && fallocate -l 100m /test/dummy && rm /test/dummy                   0.3s
 => exporting to image                                                                         0.0s
 => => exporting layers                                                                        0.0s
 => => writing image sha256:9febd9199cd67e9291df4f5fbf1504de04e8cb874428363d01ded1451bf4d20b   0.0s
 => => naming to docker.io/library/falloc_100m                                                 0.0s

docker image ls
REPOSITORY    TAG       IMAGE ID       CREATED              SIZE
falloc_100m   latest    9febd9199cd6   38 seconds ago       77.8MB
<none>        <none>    f2c36a7fbb44   About a minute ago   183MB
ubuntu        latest    c6b84b685f35   5 weeks ago          77.8MB

// 이미지 크기가 증가하지 않는다.
```

1. **불필요한 도구 설치 금지**
    
    불필요한 개발 및 디버깅 도구(vim, curl, telent, … 등)와 종속성을 제거하면 크기가 작은 효율적인 도커 이미지를 생성할 수 있다.
    

2-1. —no-install-recommands 플래그 사용

추천(recommand) 및 제안(suggested) 패키지가 자동으로 설치되는 것을 막기 위해서는 apt-get install —no-install-recommends 플래그를 사용

Dockerfile_before-optimization

```docker
FROM ubuntu:focal
RUN apt-get update && \
    apt-get install -y nginx redis-server
```

```powershell
docker image build -f Dockerfile_before-optimization -t before-optimization .
```

Dockerfile_after-optimization

```docker
FROM ubuntu:focal
RUN apt-get update && \
    apt-get install --no-install-recommends -y nginx redis-server
```

```powershell
docker image build -f Dockerfile_after-optimization -t after-optimization .
```

```powershell
docker image ls
REPOSITORY            TAG       IMAGE ID       CREATED          SIZE
after-optimization    latest    21c66a7839f7   26 seconds ago   182MB
before-optimization   latest    72d39ef98e67   2 minutes ago    182MB
falloc_100m           latest    9febd9199cd6   14 minutes ago   77.8MB
<none>                <none>    f2c36a7fbb44   15 minutes ago   183MB

// 크기 차이가 거의 나지 않는다.
```

![Untitled](docker03/docker03_2.png)

Dockerfile_after-optimization-2

```docker
FROM ubuntu:focal
RUN apt-get update && \
    apt-get install --no-install-recommends -y nginx redis-server && \
    rm -rf /var/lib/apt/lists/*
```

```powershell
docker image build -f Dockerfile_after-optimization-2 -t after-optimization-2 .

docker image ls
REPOSITORY             TAG       IMAGE ID       CREATED          SIZE
after-optimization-2   latest    c1ec622b6e56   9 seconds ago    136MB
after-optimization     latest    21c66a7839f7   8 minutes ago    182MB
before-optimization    latest    72d39ef98e67   10 minutes ago   182MB
falloc_100m            latest    9febd9199cd6   22 minutes ago   77.8MB
<none>                 <none>    f2c36a7fbb44   23 minutes ago   183MB
ubuntu                 latest    c6b84b685f35   5 weeks ago      77.8MB
```

**빌더 패턴과 다단계 도커 빌드**

**빌더 패턴**

- 최적의 크기의 도커 이미지를 생성하기 위해 사용하는 방법
- 두 개의 도커 이미지를 사용
    - 첫 번째 도커 이미지 ⇒ Builder ⇒ 소스 코드를 실행 파일로 만들기 위한 빌드 환경 제공 ⇒ 빌드에 필요한 컴파일러, 빌드 도구, 개발 종속성 등을 포함
    - 두 번재 도커 이미지 ⇒ Runtime ⇒ 첫 번째 도커 컨테이너가 생성한 실행 파일을 실행하기 위한 런타임 환경 제공 ⇒ 실행 파일, 종속성 및 런타임 도구만 포함
    - 첫 번째 도커 컨테이너가 생성한 실행 파일을 두 번째 도커 컨테이너로 전달하는 스크립트가 필요

![Untitled](docker03/docker03_3.png)

Dev dependencies : 압축되지 않은 라이브러리

Build Container ⇒ 빌드할 때 필요한 것만 존재

Runtime Container ⇒ 런타임 때 필요한 것만 존재(실행 가능한 환경에 꼭 필요한 파일과 실행되는 것만 남는다 ⇒ 파일이 가벼워진다.)

**불필요한 내용을 포함하는 예**

GO 컴파일러는 애플리케이션을 빌드할 때는 필요하지만 실행할 때는 필요로하지 않음

- 호스트에서 실행 파일을 생성해서 실행

C:\docker\build-pattern\helloworld.go

```go
package main

import "fmt"

func main() {
	fmt.Println("Hello World")
}
```

```powershell
go run .\helloworld.go
Hello World

go env -w GO111MODULE=auto

go build -o helloworld.exe .

//-o 목적 파일로
// . 현재 디렉터리에 있는 파일을

dir
디렉터리: C:\docker\build-pattern

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----      2023-09-22   오후 2:24        1897984 helloworld.exe
-a----      2023-09-22   오후 2:19             79 helloworld.go

.\helloworld.exe
Hello World

// 빌드 파일을 순수하게 목적 파일로 만드는 것
```

- Dockerfile을 정의해서 이미지를 생성

Dockerfile

```docker
FROM    golang
WORKDIR /myapp
COPY    helloworld.go .
RUN     go env -w GO111MODULE=auto
RUN     go build -o helloworld
ENTRYPOINT [ ".\helloworld" ]
```

```powershell
docker image build -t helloworld:v1

docker image ls
REPOSITORY             TAG       IMAGE ID       CREATED         SIZE
helloworld             v1        672f4bebf959   6 seconds ago   841MB

docker container run helloworld:v1

docker image pull golang

docker image ls
REPOSITORY             TAG       IMAGE ID       CREATED         SIZE
helloworld             v1        672f4bebf959   2 minutes ago   841MB
golang                 latest    8ac27c2c245e   26 hours ago    814MB

docker image pull alpine

docker image ls
REPOSITORY             TAG       IMAGE ID       CREATED         SIZE
helloworld             v1        672f4bebf959   3 minutes ago   841MB
golang                 latest    8ac27c2c245e   26 hours ago    814MB
alpine                 latest    7e01a0d0a1dc   6 weeks ago     7.34MB

//alpine => 꼭 필요한 linux만 담아놓은 linux
```

helloworld 이미지를 이용해서 실행한 컨테이너의 /myapp/helloworld 실행 파일을 호스트로 복사

```powershell
docker container run -it --entrypoint="/bin/bash" helloworld:v1

// ctrl p q

docker container ls
CONTAINER ID   IMAGE           COMMAND       CREATED          STATUS          PORTS     NAMES
0027120a3bbb   helloworld:v1   "/bin/bash"   21 seconds ago   Up 20 seconds             trusting_aryabhata

docker container cp 0027120a3bbb:/myapp/helloworld .
Successfully copied 1.8MB to C:\docker\build-pattern\.

dir
디렉터리: C:\docker\build-pattern

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----      2023-09-22   오후 2:33            154 Dockerfile
-a----      2023-09-22   오후 2:33        1802816 helloworld
-a----      2023-09-22   오후 2:26        1897984 helloworld.exe
-a----      2023-09-22   오후 2:19             79 helloworld.go
```

Docker-runtime

```docker
FROM    alpine
WORKDIR /myapp
COPY    helloworld .
ENTRYPOINT [ ".\helloworld" ]
```

```powershell
docker image build -f Dockerfile-runtime -t helloworld:v2 .

docker image ls
REPOSITORY             TAG       IMAGE ID       CREATED          SIZE
helloworld             v2        8c7fb45da89f   18 seconds ago   9.14MB
helloworld             v1        672f4bebf959   13 minutes ago   841MB

docker container run helloworld:v2
Hello World
```

Dockerfile-builder

```docker
FROM    golang
WORKDIR /myapp
COPY    helloworld.go .
RUN go env -w GO111MODULE=auto
RUN go build -o helloworld
ENTRYPOINT [ ".\helloworld" ]
```

helloworld-builder.cmd

```bash
@REM //두 개의 Dockerfile을 순차적으로 빌드하는 배치 파일

docker image build -t helloworld-build -f Dockerfile-builder .
docker container create --name build-container helloworld-build
docker container cp build-container:/myapp/helloworld .
docker container rm -f build-container 

docker image build -t helloworld -f Dockerfile-runtime .
del helloworld
```

```powershell
helloworld-builder.cmd

[+] Building 0.1s (10/10) FINISHED                                                                       docker:default
 => [internal] load .dockerignore                                                                                  0.0s
 => => transferring context: 2B                                                                                    0.0s
 => [internal] load build definition from Dockerfile-builder                                                       0.0s
 => => transferring dockerfile: 193B                                                                               0.0s
 => [internal] load metadata for docker.io/library/golang:latest                                                   0.0s
 => [1/5] FROM docker.io/library/golang                                                                            0.0s
 => [internal] load build context                                                                                  0.0s
 => => transferring context: 119B                                                                                  0.0s
 => CACHED [2/5] WORKDIR /myapp                                                                                    0.0s
 => CACHED [3/5] COPY    helloworld.go .                                                                           0.0s
 => CACHED [4/5] RUN go env -w GO111MODULE=auto                                                                    0.0s
 => CACHED [5/5] RUN go build -o helloworld                                                                        0.0s
 => exporting to image                                                                                             0.0s
 => => exporting layers                                                                                            0.0s
 => => writing image sha256:672f4bebf959aef7e5e2524eb1d5e06ba7be835b2ebbf99af44f7532efde9f2a                       0.0s
 => => naming to docker.io/library/helloworld-build                                                                0.0s

C:\docker\build-pattern>docker container create --name build-container helloworld-build
23e4ff8de56171b23771cd58faceb7cb39cd7d797fc87824e69e536155665b37

C:\docker\build-pattern>docker container cp build-container:/myapp/helloworld .
Successfully copied 1.8MB to C:\docker\build-pattern\.

C:\docker\build-pattern>docker container rm -f build-container
build-container

C:\docker\build-pattern>docker image build -t helloworld -f Dockerfile-runtime .
[+] Building 0.1s (8/8) FINISHED                                                                         docker:default
 => [internal] load build definition from Dockerfile-runtime                                                       0.0s
 => => transferring dockerfile: 128B                                                                               0.0s
 => [internal] load .dockerignore                                                                                  0.0s
 => => transferring context: 2B                                                                                    0.0s
 => [internal] load metadata for docker.io/library/alpine:latest                                                   0.0s
 => [1/3] FROM docker.io/library/alpine                                                                            0.0s
 => [internal] load build context                                                                                  0.0s
 => => transferring context: 1.80MB                                                                                0.0s
 => CACHED [2/3] WORKDIR /myapp                                                                                    0.0s
 => CACHED [3/3] COPY    helloworld .                                                                              0.0s
 => exporting to image                                                                                             0.0s
 => => exporting layers                                                                                            0.0s
 => => writing image sha256:33627e86eb53f14ae889c87ef4da357e03415183fd321f63243877372bd9c74e                       0.0s
 => => naming to docker.io/library/helloworld                                                                      0.0s

C:\docker\build-pattern>del helloworld

docker image ls
REPOSITORY             TAG       IMAGE ID       CREATED          SIZE
<none>                 <none>    8c7fb45da89f   18 minutes ago   9.14MB
helloworld             latest    33627e86eb53   18 minutes ago   9.14MB
helloworld             v2        33627e86eb53   18 minutes ago   9.14MB
helloworld-build       latest    672f4bebf959   31 minutes ago   841MB
helloworld             v1        672f4bebf959   31 minutes ago   841MB
after-optimization-2   latest    c1ec622b6e56   2 hours ago      136MB
after-optimization     latest    21c66a7839f7   2 hours ago      182MB
before-optimization    latest    72d39ef98e67   2 hours ago      182MB
falloc_100m            latest    9febd9199cd6   3 hours ago      77.8MB
golang                 latest    8ac27c2c245e   27 hours ago     814MB
ubuntu                 latest    c6b84b685f35   5 weeks ago      77.8MB
alpine                 latest    7e01a0d0a1dc   6 weeks ago      7.34MB
```

**다단계 도커 빌드**

- Docker 17.05 버전에 새롭게 추가된 기능
- 하나의 Dockerfile에 여러 개의 FROM문을 사용 빌드 단계를 정의하고, —from 플래그를 사용해 각 단계에서 생성된 아티팩트 참조가 가능하도록 하는 것
- 각 단계는 0부터 순서대로 부연된 번호 또는 AS 절을 사용해 부여한 별칭을 이용할 수 있음

기존에 생성한 컨테이너와 이미지를 삭제

c:\docker\multi-state-build

```go
package main

import "fmt"

func main() {
	fmt.Println("Hello World")
}
```

Dockerfile :v1

```docker
FROM golang
WORKDIR /myapp
COPY helloworld.go .
RUN go build - o helloworld

FROM alpine
WORKDIR /myapp
COPY --from=0 /myapp/helloworld .
ENTRYPOINT [ "./helloworld" ]
```

```docker
docker image build -t mulit-state:v1 .

```

Dockerfile :v2

```docker
FROM    golang AS builder
WORKDIR /myapp
COPY    helloworld.go .
RUN     go env -w GO111MODULE=auto
RUN     go build -o helloworld

FROM alpine AS runtime
WORKDIR /myapp
COPY --from=builder /myapp/helloworld .
ENTRYPOINT [ "./helloworld" ]
```

```powershell
docker image build -t multi-state:v2 .
```

```powershell
docker image ls
REPOSITORY    TAG       IMAGE ID       CREATED          SIZE
multi-state   v1        af42fa0cc41e   59 minutes ago   9.14MB
multi-state   v2        af42fa0cc41e   59 minutes ago   9.14MB
```

```powershell
docker image build --target runtime -t multi-state:runtime .

docker image build --target builder -t multi-state:builder .

docker image ls
REPOSITORY    TAG       IMAGE ID       CREATED             SIZE
multi-state   runtime   af42fa0cc41e   About an hour ago   9.14MB
multi-state   v1        af42fa0cc41e   About an hour ago   9.14MB
multi-state   v2        af42fa0cc41e   About an hour ago   9.14MB
multi-state   builder   7adbadcc6003   About an hour ago   841MB
```

```powershell
docker container run multi-state:runtime
Hello World

docker container run multi-state:builder
```

빌드 패턴→ 최소 2개의 도커 파일과 shell script가 무조건 있어야한다. 

다단계 → 하나의 도커 파일만 있어도 된다.

⇒ 빌드 패턴보다는 다단계가 더 좋다.

도커 17이상이면 다단계를 사용하는 것이 좋다.

### **Dockerfile 모범 사례**

도커 이미지 빌드 시간 단축, 이미지 크기 감소, 보안 강화 및 유지 관리 가능성을 보장

1. **적절한 베이스 이미지 사용**

1-1. 도커 허브 공식 이미지를 사용

도커 허브의 공식 이미지는 모범 사례를 따르고 문서화되어 있으며 보안 패치가 적용되어 있다.

예) 

Inefficient Dockerfile

---

FROM ubuntu

RUN apt-get update && apt-get install -y openjdk-8-jdk

Efficient Dockerfile

---

FROM openjdk

1-2. 특정 버전의 태그 사용

프로덕션 환경을 위한 도커 이미지를 빌드할 때 베이스 이미지의 latest tag를 사용하면 하위 호환성을 제공하지 않을 경우 문제가 될 수 있다.

예) 

Inefficient Dockerfile

---

FROM openjdk:latest

Efficient Dockerfile

---

FROM openjdk:8

1-3. 최소 크기의 이미지를 사용

최소 크기 버전의 부모(베이스) 이미지를 사용 → 최소 크기의 도커 이미지를 생성

alpine linux 이미지를 중심으로 빌드된 최소 크기 이미지 또는 빌드 도구가 포함된 JDK 대신 JRE를 사용하여 어플리케이션을 실행해야한다.

예) 

Inefficient Dockerfile

---

FROM openjdk:8

⇒ 488MB

Efficient Dockerfile

---

FROM openjdk:8-jre-alpine

⇒ 84.9MB

1. **루트가 아닌 사용자로 컨테이너를 실행**

도커 컨테이너는 기본적으로 루트(id=0)인 사용자로 실행 

⇒ 해커가 도커 컨테이너 내부에서 실행되는 어플리케이션을 해킹한 후 도커 호스트에 대한 루트 액세스 권한을 획득할 수 있으므로 프로덕션 환경에서 루트 사용자로 도커 컨테이너를 실행하는 것은 나쁜 보안 관행으로 간주

응용 프로그램 실행에 필요한 최소한의 권한만 갖도록 최소 권한의 원칙을 준수해야한다.

2-1. —user(또는 -u) 옵션을 사용

```powershell
docker container run -it --rm --user=9999 ubuntu

Unable to find image 'ubuntu:latest' locally
latest: Pulling from library/ubuntu
445a6a12be2b: Already exists
Digest: sha256:aabed3296a3d45cede1dc866a24476c4d7e093aa806263c27ddaadbdce3c1054
Status: Downloaded newer image for ubuntu:latest
I have no name!@b09ce133830c:/$
I have no name!@b09ce133830c:/$ id
uid=9999 gid=0(root) groups=0(root)
```

2-2. USER 지시문 사용

```docker
FROM ubuntu
RUN apt-get update
RUN useradd demo-user
USER demo-user
CMD whoami
```

```powershell
docker image build --target runtime -t multi-state:runtime .

docker image ls
REPOSITORY    TAG       IMAGE ID       CREATED          SIZE
user-test     latest    f7c86135870e   13 seconds ago   122MB
multi-state   runtime   af42fa0cc41e   2 hours ago      9.14MB
multi-state   v1        af42fa0cc41e   2 hours ago      9.14MB
multi-state   v2        af42fa0cc41e   2 hours ago      9.14MB
multi-state   builder   7adbadcc6003   2 hours ago      841MB

docker container run --rm user-test
demo-user

docker container run -it --rm user-test /bin/bash
demo-user@b139f8f25803:/$ id
uid=1000(demo-user) gid=1000(demo-user) groups=1000(demo-user)
```
