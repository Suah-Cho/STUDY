# docker_04

### 빌드 컨텍스트(build context)

- 도커 이미지를 생성하는데 필요한 파일, 소스 코드, 메타 데이터(Dockerfile, .dockerignore 등) 등을 담고 있는 디렉터리
- Dockerfile이 존재하는 디렉터리
- 빌드 컨텍스트는 docker build 명령어의 마지막에 지정한 위치에 있는 파일 전체를 포함
- Github과 같은 외부 URL에서 Dockerfile을 읽어 들인다면 해당 저장소에 있는 파일과 서브 모듈을 포함
- 단순 파일뿐 아니라 하위 디렉터리도 전부 포함하게 되므로 빌드에 불필요한 파일이 포함된다면 빌드 속도가 느려지고, 호스트의 메모리가 지나치게 점유할 수 있게 된다.
- .dockerignore 파일을 작성하면 명시된 이름의 파일을 빌드 시 컨텍스트에서 제외
    - 불필요한 파일 ⇒ 빌드 시간을 단축하고 네트워크 컨텍스트에서 제외
    - 기밀성을 요하는 파일
- .dockerignore 파일은 Dockerfile과 동일한 위치에 저장
    
    ![image](https://github.com/Suah-Cho/STUDY/assets/102336763/b26b4993-48cf-437a-a537-fc78c3a24e8b)


⇒ dockerignore파일은 용량을 줄여주는 측면도 있지만 보안적인 측면도 존재한다.

```powershell
cd /docker
code .
```

Dockerfile

```docker
FROM ubuntu 
RUN apt-get update
RUN useradd demo-user
CMD ["/bin/bash"]
```

password.txt

```docker
this is password
```

c:/docker/tmp 디렉터리 생성

cd c:/docker

sample.md

```docker
this is smaple.md
```

README.md

```docker
this is readme.md
```

c:/docker/.dockerignore 생성

```docker
build-pattern/
multi-state-build/
tmp/
webserver/
*.md
*.go
!README.md
password.txt
```

```powershell
docker image build -t usertest .
[+] Building 2.8s (7/7) FINISHED                                                         docker:default
 => [internal] load build definition from Dockerfile                                               0.0s
 => => transferring dockerfile: 111B                                                               0.0s
 => [internal] load .dockerignore                                                                  0.0s
 => => transferring context: 130B                                                                  0.0s
 => [internal] load metadata for docker.io/library/ubuntu:latest                                   2.7s
 => [1/3] FROM docker.io/library/ubuntu@sha256:aabed3296a3d45cede1dc866a24476c4d7e093aa806263c27d  0.0s
 => => resolve docker.io/library/ubuntu@sha256:aabed3296a3d45cede1dc866a24476c4d7e093aa806263c27d  0.0s
 => CACHED [2/3] RUN apt-get update                                                                0.0s
 => CACHED [3/3] RUN useradd demo-user                                                             0.0s
 => exporting to image                                                                             0.0s
 => => exporting layers                                                                            0.0s
 => => writing image sha256:0f901e2a1d59f13b77c06ace5684db04a669b065a1732c62072c6dcbad149c8a       0.0s
 => => naming to docker.io/library/usertest                                                        0.0s
```

Dockerfile 수정

```docker
FROM    ubuntu 
RUN     apt-get update
RUN     mkdir /myapp
WORKDIR /myapp
COPY    * /myapp/
CMD     ["/bin/bash"]
```

```powershell
docker container run -it -rm usertest /bin/bash
root@8b7fb53a7105:/myapp# ls
Dockerfile  README.md
```

### Dockerfile 명령어

**ENV**

- Dockerfile에서 사용할 환경 변수를 지정
- ENV 환경변수 이름 환경 변수 값 형식으로 설정
    
    ex) ENV workspace /workspace
    
- 설정한 환경변수는 $(환경변수 이름) 또는 $환경변수 이름 형태로 Dockerfile, 이미지, 이미지로 생성한 컨테이너에서 사용 가능
- docker container run 명령어의 -e 옵션을 이용해서 같은 이름의 환경 변수 값을 덮어 쓸 수 있다.

c:/docker/env/Dockerfile

```docker
FROM    ubuntu
ENV     WORKSPACE /myapp
RUN     mkdir ${WORKSPACE}
WORKDIR ${WORKSPACE}
RUN     touch ${WORKSPACE}/mytouchfile
```

```powershell
cd env
docker image build -t envimg .
docker container run -itd envimg /bin/bash
// 실행한 컨테이너에서 쉘을 실행
3053353ee83b84b5ee919b491e59f4c49e7190c24e3c21a32b755454da84d277

docker container attach 3053353ee83b84b5ee919b491e59f4c49e7190c24e3c21a32b755454da84d2770
// 실행되고 있는 컨테이너로 attach
root@3053353ee83b:/myapp# //해당 컨테이너로 접속(attach)했을 때 WORKDIR로 설정한 디렉터리로 이동
root@3053353ee83b:/myapp# echo $WORKSPACE  // Dockerfile 에 ENV WORKSPACE /myapp로 설정한 환경 변수를 확인
/myapp  // Dockerfile에 touch ${WORKSPACE}/mytouchfile 명령어로 만들어진 파일
root@3053353ee83b:/myapp# ls
mytouchfile
```

```powershell
docker container run -itd -e **WORKSPACE=/temp** envimg /bin/bash
0c8d3a7a1cbf6f5e5efde6ac585234874b77326782c141c3fb42715255e35470
// **WORKSPACE=/temp** 컨테이너가 실행될 때 사용된다.

docker container attach 0c8
root@0c8d3a7a1cbf:/myapp# ls
mytouchfile
root@0c8d3a7a1cbf:/myapp# ls /temp
ls: cannot access '/temp': No such file or directory
root@0c8d3a7a1cbf:/myapp# echo $WORKSPACE
/temp

// ENV     WORKSPACE /myapp 이미 컨테이너가 실행될 때 설정되어 있는 것 -> 이미지에 만들어짐
```

```python
import os

uname_value = os.environ.get('UNAME')
uage_value = os.environ.get('UAGE')

if uname_value is not None :
    print(f"UNAME is {uname_value}")
else :
    print("UNAME is not set")

if uage_value is not None :
    print(f"UAGE is {uage_value}")
else :
    print("UAGE is not set")
```

```powershell
cd ../env_python
python myapp.py
UNAME is not set

set UNAME=suah
python myapp.py
UNAME is suah

//python 수정 후
set UNAME=홍길동
python myapp.py
UNAME is 홍길동
UAGE is not set
```

컨테이너 내부에서 실행되는 프로그램의 외부에서 입력된 값의 실행이 필요한 경우 -e 옵션을 사용하여 환경변수를 변경하도록 하면 된다.

```docker
FROM    python
ENV     UNAME Hong Gild-Dong
WORKDIR /app
COPY    myapp.py .
CMD     ["python", "myapp.py"]
```

```powershell
docker image build -t myapp:py .

docker container run myapp:py
UNAME is Hong Gild-Dong
UAGE is not set

docker container run -e UNAME="Cho Suah" -e UAGE=24 myapp:py
UNAME is Cho Suah
UAGE is 24

docker container run -it -e UNAME="Cho Suah" -e UAGE=24 myapp:py /bin/bash
root@ce70d0420bb5:/app# set
UAGE=24
UID=0
UNAME='Cho Suah'
_=seet
```

**VOLUME ⇒ 파일이 저장되는 곳**

- 빌드된 이미지로 컨테이너를 생성했을 때 호스트와 공유할 컨테이너 내부의 디렉터리를 설정하는 것
- 컨테이너에서 VOLUME을 사용하면 컨테이너를 실행할 때 -v 또는  —volume 옵션을 사용하여 호스트의 볼륨을 연결하거나 볼륨 컨테이너를 생성해 연결해주어야 한다.
- VOLUME 명령을 사용하는 주요 목적
    - 데이터 보존
    - 데이터 공유
    - 데이터 컨테이너와 애플리케이션 코드를 분리

c: /docker/volume/Dockerfile

```docker
FROM ubuntu
RUN mkdir /home/share
RUN echo test >> /home/share/testfile
```

```powershell
docker iamge build -t myvolume:1.0 .

docker container run -it --rm myvolume:1.0 /bin/bash
root@03872b36a0d1:/# ls /home/share/
testfile

root@03872b36a0d1:/# echo test2 >> /home/share/test2 //새로운 파일을 생성한 후 컨테이너를 종료
root@03872b36a0d1:/# ls /home/share/
test2  testfile

docker container run -it --rm myvolume:1.0 /bin/bash
root@e09b45d7aea8:/# ls /home/share
testfile // 파일이 사라지고 없다. => 컨테이너는 데이터를 보존하지 않는다.
```

Dockerfile 수정

```docker
FROM ubuntu
RUN mkdir /home/share
RUN echo test >> /home/share/testfile
VOLUME /home/share
```

```powershell
docker image build -t myvolume:2.0 .

mkdir data // 볼륨 맵핑에 사용할 디렉터리 생성

root@303a8fe37b8b:/# ls /home/share
root@303a8fe37b8b:/# echo test2 >> /home/share/test2
root@303a8fe37b8b:/# ls /home/share
test2
root@303a8fe37b8b:/# mkdir /home/share/tmp
root@303a8fe37b8b:/# ls -l /home/share
total 0
-rw-r--r-- 1 root root    6 Sep 25 03:08 test2
drwxr-xr-x 1 root root 4096 Sep 25 03:09 tmp
root@303a8fe37b8b:/# exit
exit

dir data
C 드라이브의 볼륨에는 이름이 없습니다.
 볼륨 일련 번호: D0A5-3978

 C:\docker\volume\data 디렉터리

2023-09-25  오후 12:09    <DIR>          .
2023-09-25  오후 12:09    <DIR>          ..
2023-09-25  오후 12:08                 6 test2
2023-09-25  오후 12:09    <DIR>          tmp
               1개 파일                   6 바이트
               3개 디렉터리  123,220,983,808 바이트 남음

// 새로운 컨테이너 생성
docker container run -it --rm -v c:\docker\volume\data\:/home/share/ myvolume:2.0 /bin/bash
root@97938e633911:/# ls /home/share
test2  tmp  // 동일한 파일이 들어있다.
```

### 컨테이너 관련 명령어

```powershell
docker container run -it --rm --name mycontainerv1 myvolume:1.0 /bin/bash
docker container run -it --rm --name mycontainer myvolume:2.0 /bin/bash
docker container run -it --rm --name othercontainer myvolume:2.0 /bin/bash

docker container ls
CONTAINER ID   IMAGE          COMMAND       CREATED          STATUS          PORTS     NAMES
5df7c6a387bc   myvolume:1.0   "/bin/bash"   22 seconds ago   Up 21 seconds             mycontainerv1
488dbb6d8c98   myvolume:2.0   "/bin/bash"   3 minutes ago    Up 3 minutes              othercontainer
e5ad1ea79966   myvolume:2.0   "/bin/bash"   3 minutes ago    Up 3 minutes              mycontainer
```

- 특정 ID를 가진 컨테이너를 중지

```powershell
docker container stop 컨테이너 id
```

- 특정 이름을 가진 컨테이너를 중지

```powershell
docker container stop 컨테이너 이름
```

- 모든 실행 중인 컨테이너를 중지

```powershell
docker container stop $(docker container ls -q)
```

- 동일 이미지로 생성, 실행된 컨테이너를 중지

```powershell
docker container ls --filter "ancestor=myvolume:2.0"
```

```powershell
docker container ls --filter "ancestor=myvolume:2.0
CONTAINER ID   IMAGE          COMMAND       CREATED         STATUS         PORTS     NAMES
488dbb6d8c98   myvolume:2.0   "/bin/bash"   4 minutes ago   Up 4 minutes             othercontainer
e5ad1ea79966   myvolume:2.0   "/bin/bash"   4 minutes ago   Up 4 minutes             mycontainer

docker container stop $(docker container ls --filter "ancestor=myvolume:2.0" -q)
488dbb6d8c98
e5ad1ea79966

docker container ls
CONTAINER ID   IMAGE          COMMAND       CREATED         STATUS         PORTS     NAMES
5df7c6a387bc   myvolume:1.0   "/bin/bash"   3 minutes ago   Up 3 minutes             mycontainerv1
```

**이미지 태깅**

```powershell
docker image ls
REPOSITORY    TAG       IMAGE ID       CREATED             SIZE
myvolume      2.0       8940e84abbe3   About an hour ago   77.8MB

docker image build -t myvolume:2.0 .
[+] Building 2.6s (7/7) FINISHED                                                         docker:default
 => [internal] load .dockerignore                                                                  0.0s
 => => transferring context: 2B                                                                    0.0s
 => [internal] load build definition from Dockerfile                                               0.0s
 => => transferring dockerfile: 130B                                                               0.0s
 => [internal] load metadata for docker.io/library/ubuntu:latest                                   2.6s
 => [1/3] FROM docker.io/library/ubuntu@sha256:aabed3296a3d45cede1dc866a24476c4d7e093aa806263c27d  0.0s
 => => resolve docker.io/library/ubuntu@sha256:aabed3296a3d45cede1dc866a24476c4d7e093aa806263c27d  0.0s
 => CACHED [2/3] RUN mkdir /home/share                                                             0.0s
 => CACHED [3/3] RUN echo test >> /home/share/testfile                                             0.0s
 => exporting to image                                                                             0.0s
 => => exporting layers                                                                            0.0s
 => => writing image sha256:8940e84abbe3a3645e2adadb3760e10a4f759b871753fae7224460c01a3f7c9c       0.0s
 => => naming to docker.io/library/myvolume:2.0

// Dockerfile 변경이 없어서 캐시를 사용했고, 그 결과 이미지를 새롭게 만들지 않았다.

docker image ls
REPOSITORY    TAG       IMAGE ID       CREATED             SIZE
myvolume      1.0       78d252af16de   About an hour ago   77.8MB

docker image build --no-cache -t myvolume:2.0 .
[+] Building 1.6s (7/7) FINISHED                                                         docker:default
 => [internal] load .dockerignore                                                                  0.0s
 => => transferring context: 2B                                                                    0.0s
 => [internal] load build definition from Dockerfile                                               0.0s
 => => transferring dockerfile: 130B                                                               0.0s
 => [internal] load metadata for docker.io/library/ubuntu:latest                                   0.8s
 => CACHED [1/3] FROM docker.io/library/ubuntu@sha256:aabed3296a3d45cede1dc866a24476c4d7e093aa806  0.0s
 => => resolve docker.io/library/ubuntu@sha256:aabed3296a3d45cede1dc866a24476c4d7e093aa806263c27d  0.0s
 => [2/3] RUN mkdir /home/share                                                                    0.3s
 => [3/3] RUN echo test >> /home/share/testfile                                                    0.4s
 => exporting to image                                                                             0.0s
 => => exporting layers                                                                            0.0s
 => => writing image sha256:bd95682bf9f0b981f7e8f9cfd65a51b4cf64918d7f662d008c78cdebb66354dd       0.0s
 => => naming to docker.io/library/myvolume:2.0                                                    0.0s

docker image ls
REPOSITORY    TAG       IMAGE ID       CREATED              SIZE
myvolume      2.0       bd95682bf9f0   30 seconds ago       77.8MB
<none>        <none>    8940e84abbe3   About an hour ago    77.8MB

docker image ls --filter="dangling=true"
REPOSITORY   TAG       IMAGE ID       CREATED             SIZE
<none>       <none>    8940e84abbe3   About an hour ago   77.8MB

docker image tag myvolume:2.0 myvolume:OLD
docker image ls
REPOSITORY    TAG       IMAGE ID       CREATED             SIZE
myvolume      2.0       bd95682bf9f0   3 minutes ago       77.8MB
myvolume      OLD       bd95682bf9f0   3 minutes ago       77.8MB

docker image build --no-cache -t myvolume:2.0 .

docker image ls
REPOSITORY    TAG       IMAGE ID       CREATED             SIZE
myvolume      2.0       8340447b8059   4 seconds ago       77.8MB
myvolume      OLD       bd95682bf9f0   3 minutes ago       77.8MB

// 새롭게 이미지가 생성된다.
// tag 명령어로 복사한 이미지는 유지된다.
```

### Docker Hub

Registry : 저장소 ( Docker Hub)

Repository : namespace/imgname : tag

```
docker image tag myvolume:latest suahcho/myvolume:latest
docker image ls
REPOSITORY         TAG       IMAGE ID       CREATED       SIZE
suahcho/myvolume   latest    8340447b8059   2 hours ago   77.8MB

docker login
Authenticating with existing credentials...
Login Succeeded

docker image push suahcho/myvolume:latest
The push refers to repository [docker.io/suahcho/myvolume]
2c5d47f0e9fc: Pushed
2085a6849d26: Pushed
dc0585a4b8b7: Mounted from library/ubuntu
latest: digest: sha256:1267486457d330260541db041d2048ebdee4284907e4719bf5292f223db82f80 size: 943
```

![image](https://github.com/Suah-Cho/STUDY/assets/102336763/8b019e14-e675-4a27-b096-d72d5e134f94)

|Docker|Compose|Swarm|
|---|---|---|
|단일 호스트 단일 컨테이너|한 pc에서 멀티 컨테이너 관리 용이|멀티 호스트에서 cluster를 만들어서 멀티 컨테이너를 관리|

```
docker container run -itd --rm myvolume:latest /bin/bash
9ede8d83ef4075b691110ea88f8878f80952eddd4b8dcc8f21c25e480e0a2c78

docker container exec 9ede ls -l /home/share/
total 4
-rw-r--r-- 1 root root 5 Sep 25 03:45 testfile

docker container cp .\data\ 9ede:/home/share
Successfully copied 3.07kB to 9ede:/home/share

docker container exec 9ede ls -l /home/share/
total 8
drwxr-xr-x 3 root root 4096 Sep 25 03:09 data
-rw-r--r-- 1 root root    5 Sep 25 03:45 testfile

docker container cp .\test.txt 9ede:/home/share/
Successfully copied 2.05kB to 9ede:/home/share/

docker container exec 9ede ls -l /home/share/
total 12
drwxr-xr-x 3 root root 4096 Sep 25 03:09 data
-rwxr-xr-x 1 root root    9 Sep 25 05:43 test.txt
-rw-r--r-- 1 root root    5 Sep 25 03:45 testfile

dir
 C 드라이브의 볼륨에는 이름이 없습니다.
 볼륨 일련 번호: D0A5-3978

 C:\docker\volume 디렉터리

2023-09-25  오후 02:42    <DIR>          .
2023-09-25  오후 02:42    <DIR>          ..
2023-09-25  오후 12:09    <DIR>          data
2023-09-25  오전 11:29                93 Dockerfile
2023-09-25  오후 02:43                 9 test.txt
               2개 파일                 102 바이트
               3개 디렉터리  122,899,161,088 바이트 남음

docker container cp 9ede:/home/share/testfile .
Successfully copied 2.05kB to C:\docker\volume\.

dir
 C 드라이브의 볼륨에는 이름이 없습니다.
 볼륨 일련 번호: D0A5-3978

 C:\docker\volume 디렉터리

2023-09-25  오후 02:49    <DIR>          .
2023-09-25  오후 02:49    <DIR>          ..
2023-09-25  오후 12:09    <DIR>          data
2023-09-25  오전 11:29                93 Dockerfile
2023-09-25  오후 02:43                 9 test.txt
2023-09-25  오후 12:45                 5 testfile
               3개 파일                 107 바이트
               3개 디렉터리  122,898,522,112 바이트 남음

docker container cp 9ede:/home/share/data/ .\temp\
// 컨테이너 내부에 있는 data 디렉터리 아래의 내용을 호스트의 temp 디렉터리 아래로 복사

```
