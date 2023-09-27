# Docker_05

### 사용 현황 조회

```powershell
docker container rm -f $(docker container ls -aq)
docker image rm $(docker image -q)

//모든 리소스 삭제
```

**컨테이너 리소스 사용 현황**

```powershell
docker container run -itd --name myubuntu ubuntu
Unable to find image 'ubuntu:latest' locally
latest: Pulling from library/ubuntu
445a6a12be2b: Already exists
Digest: sha256:aabed3296a3d45cede1dc866a24476c4d7e093aa806263c27ddaadbdce3c1054
Status: Downloaded newer image for ubuntu:latest
247e20cbea8c5ab8140a9196a6c392f7e7b63f39f7d49d3f9163de129ec3f84a

docker container ls
CONTAINER ID   IMAGE     COMMAND       CREATED          STATUS          PORTS     NAMES
247e20cbea8c   ubuntu    "/bin/bash"   42 seconds ago   Up 41 seconds             myubuntu

docker container -d -p 80 --name mynginx nginx
17fae8b20e6383d525ac43a35cce7fe986ea7276dcc893e9e95eae1617d35780

```

```powershell
docker container stats
CONTAINER ID   NAME         CPU %     MEM USAGE / LIMIT     MEM %     NET I/O           BLOCK I/O   PIDS
4d5e1fe80889   othernginx   0.00%     7.309MiB / 12.27GiB   0.06%     12.8kB / 5.79kB   0B / 0B     9

CONTAINER ID   NAME         CPU %     MEM USAGE / LIMIT     MEM %     NET I/O           BLOCK I/O   PIDS
4d5e1fe80889   othernginx   0.00%     7.309MiB / 12.27GiB   0.06%     15.7kB / 5.79kB   0B / 0B     9
```

**디스크 이용 현황**

```powershell
docker system df
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          2         2         264.5MB   0B (0%)
Containers      3         3         2.19kB    0B (0%)
Local Volumes   0         0         0B        0B
Build Cache     110       0         612MB     612MB

docker system df -v
Images space usage:

REPOSITORY   TAG       IMAGE ID       CREATED       SIZE      SHARED SIZE   UNIQUE SIZE   CONTAINERS
nginx        latest    61395b4c586d   5 days ago    187MB     0B            186.6MB       2
ubuntu       latest    c6b84b685f35   5 weeks ago   77.8MB    0B            77.82MB       1

Containers space usage:

CONTAINER ID   IMAGE     COMMAND                   LOCAL VOLUMES   SIZE      CREATED         STATUS         NAMES
4d5e1fe80889   nginx     "/docker-entrypoint.…"   0               1.09kB    3 minutes ago   Up 3 minutes   othernginx
17fae8b20e63   nginx     "/docker-entrypoint.…"   0               1.09kB    5 minutes ago   Up 5 minutes   mynginx
247e20cbea8c   ubuntu    "/bin/bash"               0               0B        8 minutes ago   Up 8 minutes   myubuntu

Local Volumes space usage:

VOLUME NAME   LINKS     SIZE

Build cache usage: 612MB

CACHE ID       CACHE TYPE     SIZE      CREATED        LAST USED        USAGE     SHARED
ipe62m9pgw02   regular        0B        4 days ago     4 days ago       1         false
d5lo6aghsox0   regular        0B        4 days ago     4 days ago       1         false
rklv8ol0cwe9   regular        0B        4 days ago     4 days ago       1         false
mg90t8fnarbp   regular        0B        4 days ago     4 days ago       1         false
xrhxep1lpw79   regular        0B        4 days ago     4 days ago       1         false
oagskwi0fv69   regular        0B        4 days ago     4 days ago       1         false
szr8nscf6o00   regular        0B        4 days ago     4 days ago       1         false
le1rono3684f   regular        0B        4 days ago     4 days ago       1         false
ipts4ld0qyzs   regular        370B      4 days ago     4 days ago       2         false
zpeb7yjn6bfa   regular        0B        4 days ago     4 days ago       1         false
2awyrzu8ozoq   regular        370B      4 days ago     4 days ago       1         false
ui4f8do0ike1   regular        370B      4 days ago     4 days ago       1         false
t12zqmf5uxjv   regular        0B        4 days ago     4 days ago       2         false
ru7s0jipu46y   regular        373B      4 days ago     4 days ago       2         false
m5wy41icxiql   regular        0B        4 days ago     4 days ago       1         false
v2b8jdafxcho   regular        373B      4 days ago     4 days ago       2         false
0t1gjui648ku   regular        0B        4 days ago     4 days ago       1         false
hc5e0rqc1ye4   regular        373B      4 days ago     4 days ago       1         false
qgw3kem1n1zl   regular        0B        4 days ago     4 days ago       5         false
ur887oxyzsyg   regular        44.1MB    3 days ago     3 days ago       1         false
z8azw5dg5xe3   regular        108MB     3 days ago     3 days ago       1         false
bvcoxwj36dg5   regular        240B      3 days ago     3 days ago       3         false
b3gkdz5agh9n   regular        0B        3 days ago     3 days ago       1         false
mmvjwkgh49xb   source.local   240B      3 days ago     3 days ago       5         false
c4tdlzzbhd1k   regular        7B        3 days ago     3 days ago       2         false
gmky7f4dsiej   regular        0B        3 days ago     3 days ago       3         false
qi0v2c7433wn   regular        105MB     3 days ago     3 days ago       1         false
xq0vxcjyii1u   regular        0B        3 days ago     3 days ago       1         false
q8crffankydf   regular        0B        3 days ago     3 days ago       9         true
jy2ojvb50voo   regular        0B        3 days ago     3 days ago       1         false
xmypq1xbgur9   regular        109MB     3 days ago     3 days ago       1         false
kxl4yej48brb   regular        109MB     3 days ago     3 days ago       1         false
srmwkqqua9f6   source.local   116B      3 days ago     3 days ago       19        false
pvtfbmkpnr3l   regular        63.1MB    3 days ago     3 days ago       1         false
8r5pvnvw2nyp   source.local   0B        3 days ago     3 days ago       19        false
f6f3zisa53th   regular        0B        3 days ago     3 days ago       4         false
tdi0f50ox9u8   regular        0B        3 days ago     3 days ago       1         false
lzaygobui4sg   regular        0B        3 days ago     3 days ago       1         false
xi5ymaingbrb   regular        0B        3 days ago     3 days ago       1         false
o051jyb9yz2y   regular        0B        3 days ago     3 days ago       1         false
6rh2qcvz07e1   regular        0B        3 days ago     3 days ago       1         false
chvk12iinj8q   regular        0B        3 days ago     3 days ago       1         false
uccbn8z1y7jw   regular        0B        3 days ago     3 days ago       1         false
4jaqfovsrsf6   regular        79B       3 days ago     3 days ago       2         false
0m3igwxqhsds   regular        0B        3 days ago     3 days ago       1         false
pspvr8gm81ap   regular        0B        3 days ago     3 days ago       2         false
lojdxpmlv1l1   regular        79B       3 days ago     3 days ago       1         false
lsmbdwb8qa44   source.local   118B      3 days ago     3 days ago       9         false
ykjx6g4my2v7   source.local   79B       3 days ago     3 days ago       8         false
it1evumj8yq6   source.local   0B        3 days ago     3 days ago       9         false
oimq7o7bvzrt   regular        17B       3 days ago     3 days ago       2         false
k9l7dvxr5emh   regular        26.8MB    3 days ago     3 days ago       4         false
voz98ls08934   regular        1.8MB     3 days ago     3 days ago       7         false
qlqqmrd61fqp   source.local   79B       3 days ago     3 days ago       5         false
esl5k50qzwf5   source.local   0B        3 days ago     3 days ago       6         false
zydx855daxqx   source.local   207B      3 days ago     3 days ago       6         false
zt5stqx7fv72   regular        44.1MB    3 days ago     3 days ago       2         false
jx8nn5y4b7o9   regular        329kB     3 days ago     24 hours ago     2         false
wz6dtdgowd4h   regular        0B        24 hours ago   24 hours ago     1         false
xi38opk661g3   source.local   370B      4 days ago     24 hours ago     10        false
9wolzt7e5fdv   regular        0B        24 hours ago   24 hours ago     1         false
gfgeqg4gy9uq   regular        226B      24 hours ago   24 hours ago     1         false
96pipk2y4cow   source.local   0B        4 days ago     24 hours ago     13        false
bmoc7h0zewag   source.local   0B        4 days ago     24 hours ago     13        false
uoxn9mjwk3vk   regular        0B        23 hours ago   23 hours ago     1         false
o9hhkpdm9es0   regular        0B        23 hours ago   23 hours ago     1         false
131qx1qczeel   source.local   130B      23 hours ago   23 hours ago     1         false
xy2s1wyappnr   source.local   0B        23 hours ago   23 hours ago     1         false
o6v1038a34m8   regular        0B        23 hours ago   23 hours ago     1         false
ov3raldbo4os   regular        0B        23 hours ago   23 hours ago     1         false
m7r1dqfi25vl   regular        0B        23 hours ago   23 hours ago     1         false
ps439kbt2ux5   regular        0B        23 hours ago   23 hours ago     1         false
n2rggb9nzivh   regular        0B        23 hours ago   23 hours ago     1         false
qvd8q0q8p56s   source.local   301B      23 hours ago   23 hours ago     1         false
6mf5rricwp1p   source.local   0B        23 hours ago   23 hours ago     1         false
vgvhbtgzjw6y   source.local   110B      23 hours ago   23 hours ago     1         false
ye0d0h5gz68h   regular        0B        23 hours ago   23 hours ago     1         false
p05u2dovzcw5   regular        301B      23 hours ago   23 hours ago     1         false
y40zi7c6thxh   regular        0B        22 hours ago   22 hours ago     1         false
mv5thf1qvuhv   regular        5B        22 hours ago   21 hours ago     3         false
ie95r6lwy92o   regular        5B        21 hours ago   21 hours ago     1         false
mghteokszpih   regular        0B        21 hours ago   21 hours ago     1         false
ipuzid2uk84z   regular        5B        21 hours ago   21 hours ago     1         false
x7y2ngyjrggz   regular        0B        21 hours ago   21 hours ago     1         false
08ytr2qabzt6   regular        0B        21 hours ago   21 hours ago     1         false
jajienp998mu   regular        0B        18 hours ago   18 hours ago     1         true
pgpfd35aqx9u   regular        0B        18 hours ago   18 hours ago     1         true
ojgty5hsi0iy   regular        0B        18 hours ago   18 hours ago     1         true
v25z7ss2nf38   regular        0B        18 hours ago   18 hours ago     1         true
fvn9ps5vr8fm   regular        0B        18 hours ago   18 hours ago     1         true
o2fpk9a81dy9   regular        0B        18 hours ago   18 hours ago     1         true
cwbza0rslg1d   regular        297B      18 hours ago   18 hours ago     2         false
tl8fozlowmi5   regular        0B        18 hours ago   18 hours ago     3         false
vkwxcgmj5ji0   regular        0B        18 hours ago   18 hours ago     1         false
ltkzw6yioxno   regular        253B      18 hours ago   18 hours ago     2         false
rne763snwrrj   regular        0B        18 hours ago   18 hours ago     3         true
dz1ygueha6sb   source.local   0B        18 hours ago   18 hours ago     6         false
ofowtl9pnuqp   source.local   44B       18 hours ago   18 hours ago     6         false
ouewp22ravzp   regular        253B      18 hours ago   18 hours ago     1         false
0apn0kit4nbt   source.local   297B      18 hours ago   18 hours ago     7         false
i6zg3fo8yomp   regular        259B      17 hours ago   17 hours ago     1         false
mfhiu968im96   regular        279B      17 hours ago   17 hours ago     2         false
l60c4i113mek   regular        0B        23 hours ago   17 hours ago     4         false
p35z6mks7ote   source.local   80B       17 hours ago   17 hours ago     4         false
icg6tc1zamwa   source.local   0B        17 hours ago   17 hours ago     4         false
420zx2monn82   regular        308B      17 hours ago   17 hours ago     1         false
qyisct3kx54m   source.local   279B      17 hours ago   17 hours ago     4         false
8btnbtz01qrb   regular        5B        21 hours ago   51 minutes ago   4         false
y6oykriuoxkt   source.local   0B        22 hours ago   51 minutes ago   9         false
pnmwf0mzam7p   source.local   85B       22 hours ago   51 minutes ago   9         false
```

**Formatting**

[docs.docker](https://docs.docker.com/engine/reference/commandline/ps/#format)

```powershell
docker container ls --format "{{.ID}} : {{.Command}}"
17fae8b20e63 : "/docker-entrypoint.…"
247e20cbea8c : "/bin/bash"
```

### 레지스토리 운영

**레지스트리 실행**

```powershell
docker container run -d -p 5000:5000 --name myregistry registry:2
Unable to find image 'registry:2' locally
2: Pulling from library/registry
7264a8db6415: Already exists
c4d48a809fc2: Pull complete
88b450dec42e: Pull complete
121f958bea53: Pull complete
7417fa3c6d92: Pull complete
Digest: sha256:d5f2fb0940fe9371b6b026b9b66ad08d8ab7b0d56b6ee8d5c71cb9b45a374307
Status: Downloaded newer image for registry:2
acde3d9eebc2e0aeab2cfa775461ad010d6dc976a87f8b7baf6fac76e5c3877d

docker container ls --no-trunc --format "{{.Command}}"
"/entrypoint.sh /etc/docker/registry/config.yml"
"/docker-entrypoint.sh nginx -g 'daemon off;'"

// entrypoint.sh -> 해당 컨테이너가 실행될 때, 복잡한 케이스들을 조건에 맞추어 설정&실행을 해주는 shell script
```

**도커 허브에서 ubuntu 이미지를 pull**

```powershell
docker image pull ubuntu
Using default tag: latest
latest: Pulling from library/ubuntu
Digest: sha256:aabed3296a3d45cede1dc866a24476c4d7e093aa806263c27ddaadbdce3c1054
Status: Image is up to date for ubuntu:latest
docker.io/library/ubuntu:latest

docker image ls
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
ubuntu       latest    c6b84b685f35   5 weeks ago   77.8MB
```

**이미지에서 레지스트리 정보를 태깅**

```powershell
docker image tag ubuntu localhost:5000/myubuntu

docker image ls
REPOSITORY                TAG       IMAGE ID       CREATED       SIZE
nginx                     latest    61395b4c586d   5 days ago    187MB
ubuntu                    latest    c6b84b685f35   5 weeks ago   77.8MB
localhost:5000/myubuntu   latest    c6b84b685f35   5 weeks ago   77.8MB
registry                  2         0030ba3d620c   6 weeks ago   24.1MB
```

**로컬 레지스트리로 이미지를 push**

```powershell
docker image push localhosts:5000/myubuntu
Using default tag: latest
The push refers to repository [localhost:5000/myubuntu]
dc0585a4b8b7: Pushed
latest: digest: sha256:1f77fcf82cc387f6e40e7ca28ba98f5c7241d4211481d9e5532e8ea54e0d9ad5 size: 529

// localhost:5000/myubuntu 삭제
docker image rm localhost:5000/myubuntu
docker image ls
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
nginx        latest    61395b4c586d   5 days ago    187MB
ubuntu       latest    c6b84b685f35   5 weeks ago   77.8MB
registry     2         0030ba3d620c   6 weeks ago   24.1MB

// localhost registry에서 이미지 pull
docker image pull localhost:5000/myubuntu

docker image ls
REPOSITORY                TAG       IMAGE ID       CREATED       SIZ
localhost:5000/myubuntu   latest    c6b84b685f35   5 weeks ago   77.8MB

```

### 도커에서 데이터 관리

[https://docs.docker.com/storage/](https://docs.docker.com/storage/)

![image](https://github.com/Suah-Cho/STUDY/assets/102336763/e7bd8b55-3edd-4860-9c30-c81bcd1b2aaa)


**Volume**

- 호스트의 파일 시스템 내에 특정 영역(리눅스의 경우, /var/lib/docker/volumes/)을 도커가 사용, 관리
- 도커가 아닌 다른 프로세스에서는 해당 영역 접근이 불가능
- 가장 추천하는 방식

**Bind Mount**

- 호스트의 파일 시스템 자체를 사용
- 호스트와 컨테이너가 설정 파일을 공유하거나 호스트에서 개발하고 컨테이너로 배포하는 방식으로 사용

**tmpfs mount**

- 호스트의 파일 시스템 대신 메모리에 저장하는 방식
- non-persistent data를 다룰 때는 tmpfs mount가 가장 좋음

**-v 또는 —mount 옵션**

-v  볼륨 이름 : 마운트 경로 : 옵션

![image](https://github.com/Suah-Cho/STUDY/assets/102336763/8ab24d0a-3dc6-4e68-891f-2026fe06ca7a)


—mount

⇒ -v옵션에 사용했던 것을 key값으로 정의하는 것

![image](https://github.com/Suah-Cho/STUDY/assets/102336763/8a6a06e1-e950-48ba-bbaa-2911b72ef905)


**bind mount 공유 예** 

**#1 MySQL 이미지를 이용해서 데이터베이스 컨테이너를 실행**

[https://hub.docker.com/_/mysql](https://hub.docker.com/_/mysql)

**`MYSQL_ROOT_PASSWORD` → 필수**

```powershell
docker container run -d --name wordpressdb_hostvolume -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=wordpress -v c:\docker\mysql_data:/var/lib/mysql mysql:5.7

// /var/lib/mysql MYSQL 데이터가 저장되는 기본 디렉터리
```

**#2 워드프레스 이미지를 이용해서 웹 애플리케이션 컨테이너를 실행**

[https://hub.docker.com/_/wordpress](https://hub.docker.com/_/wordpress)

```powershell
docker container run -d -e WORDPRESS_DB_PASSWORD=password --name wordpress_hostvolume --link wordpressdb_hostvolume:mysql -p 80 wordpress
```

```powershell
docker container ls
CONTAINER ID   IMAGE        COMMAND                   CREATED             STATUS             PORTS                    NAMES
d7ca584a2e6f   wordpress    "docker-entrypoint.s…"   26 seconds ago      Up 25 seconds      0.0.0.0:56962->80/tcp    wordpress_hostvolume
4de3644f6231   mysql:5.7    "docker-entrypoint.s…"   8 minutes ago       Up 8 minutes       3306/tcp, 33060/tcp      wordpressdb_hostvolume
```

**#3 호스트 볼륨을 확인**

```powershell
dir .\mysql_data
2023-09-26  오전 10:27    <DIR>          .
2023-09-26  오전 10:27    <DIR>          ..
2023-09-26  오전 10:27                56 auto.cnf
2023-09-26  오전 10:27             1,676 ca-key.pem
2023-09-26  오전 10:27             1,112 ca.pem
2023-09-26  오전 10:27             1,112 client-cert.pem
2023-09-26  오전 10:27             1,676 client-key.pem
2023-09-26  오전 10:27        79,691,776 ibdata1
2023-09-26  오전 10:27        12,582,912 ibtmp1
2023-09-26  오전 10:27             1,318 ib_buffer_pool
2023-09-26  오전 10:27        50,331,648 ib_logfile0
2023-09-26  오전 10:27        50,331,648 ib_logfile1
2023-09-26  오전 10:27    <DIR>          mysql
2023-09-26  오전 10:27    <JUNCTION>     mysql.sock [...]
2023-09-26  오전 10:27    <DIR>          performance_schema
2023-09-26  오전 10:27             1,676 private_key.pem
2023-09-26  오전 10:27               452 public_key.pem
2023-09-26  오전 10:27             1,112 server-cert.pem
2023-09-26  오전 10:27             1,680 server-key.pem
2023-09-26  오전 10:27    <DIR>          sys
2023-09-26  오전 10:27    <DIR>          wordpress
              15개 파일         192,949,854 바이트
               6개 디렉터리  116,035,239,936 바이트 남음
```

**#4. 컨테이너 삭제 후 데이터 보존 여부를 확인**

```powershell
docker container rm -f wordpress_hostvolume wordpressdb_hostvolume

dir
2023-09-26  오전 10:27    <DIR>          .
2023-09-26  오전 10:27    <DIR>          ..
2023-09-26  오전 10:27                56 auto.cnf
2023-09-26  오전 10:27             1,676 ca-key.pem
2023-09-26  오전 10:27             1,112 ca.pem
2023-09-26  오전 10:27             1,112 client-cert.pem
2023-09-26  오전 10:27             1,676 client-key.pem
2023-09-26  오전 10:27        79,691,776 ibdata1
2023-09-26  오전 10:27        12,582,912 ibtmp1
2023-09-26  오전 10:27             1,318 ib_buffer_pool
2023-09-26  오전 10:27        50,331,648 ib_logfile0
2023-09-26  오전 10:27        50,331,648 ib_logfile1
2023-09-26  오전 10:27    <DIR>          mysql
2023-09-26  오전 10:27    <JUNCTION>     mysql.sock [...]
2023-09-26  오전 10:27    <DIR>          performance_schema
2023-09-26  오전 10:27             1,676 private_key.pem
2023-09-26  오전 10:27               452 public_key.pem
2023-09-26  오전 10:27             1,112 server-cert.pem
2023-09-26  오전 10:27             1,680 server-key.pem
2023-09-26  오전 10:27    <DIR>          sys
2023-09-26  오전 10:27    <DIR>          wordpress
              15개 파일         192,949,854 바이트
               6개 디렉터리  116,028,223,488 바이트 남음

// 컨테이너가 죽어도 그래도 존재하는 것을 볼 수 있다.
```

**#5. 디렉터리 단위 공유 뿐 아니라 파일 단위의 공유도 가능하며, -v 옵션을 다중으로 사용하는 것도 가능**

```powershell
echo hello >> hello
echo hello2 >> hello2

dir
C 드라이브의 볼륨에는 이름이 없습니다.
 볼륨 일련 번호: D0A5-3978

 C:\docker 디렉터리

2023-09-26  오전 10:43    <DIR>          .
2023-09-26  오전 10:43    <DIR>          ..
2023-09-25  오전 09:45                92 .dockerignore
2023-09-25  오후 05:33    <DIR>          apache
2023-09-22  오후 03:04    <DIR>          build-pattern
2023-09-25  오전 09:42               119 Dockerfile
2023-09-25  오전 10:35    <DIR>          env
2023-09-25  오전 11:22    <DIR>          env_python
2023-09-25  오후 04:26    <DIR>          gugudan
2023-09-26  오전 10:43                 8 hello
2023-09-26  오전 10:43                 9 hello2
2023-09-21  오후 02:57               373 main.go
2023-09-22  오후 04:40    <DIR>          multi-state-build
2023-09-26  오전 10:27    <DIR>          mysql_data
2023-09-25  오후 03:35    <DIR>          mywebserver
2023-09-25  오후 03:14    <DIR>          nginx
2023-09-25  오전 09:34                16 password.txt
2023-09-25  오전 09:36                17 README.md
2023-09-25  오전 09:36                14 sample.md
2023-09-25  오전 09:34    <DIR>          tmp
2023-09-26  오전 08:29    <DIR>          volume
2023-09-26  오전 08:29    <DIR>          volume - 복사본
2023-09-22  오후 12:48    <DIR>          webserver
               8개 파일                 648 바이트
              15개 디렉터리  116,014,018,560 바이트 남음

type hello
hello

type hello2
hello2

// echo '>' -> 덮어쓰기 '>>' -> 추가 
```

```powershell
docker container run -it --name filevolume -v c:\docker\hello:/hello -v c:\docker\hello2:/hello2 ubuntu
root@05d4f1760b05:/# ls
bin   dev  hello   home  lib32  libx32  mnt  proc  run   srv  tmp  var
boot  etc  hello2  lib   lib64  media   opt  root  sbin  sys  usr
root@05d4f1760b05:/# cat hello && cat hello2
hello
hello2
root@05d4f1760b05:/# echo HELLO > /hello 
root@05d4f1760b05:/# cat hello && cat hello2
HELLO
HELLO2
root@05d4f1760b05:/# exit
exit

docker container ls
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

type hello && type hello2
HELLO
HELLO2
// 컨테이너 내부에서 hello, hello2파일에 추가한 내용이 그대로 유지 => 파일이 공유되고 있다.
```

**볼륨 컨테이너 공유 예**

![image](https://github.com/Suah-Cho/STUDY/assets/102336763/44bd3095-f109-4bba-b777-0a7279b2141d)


**volume 예**

**#1. 볼륨 생성**

```powershell
docker volume create myvolume
docker volume ls
DRIVER    VOLUME NAME
local     myvolume
```

**#2. 생성한 볼륨을 사용하는 컨테이너를 실행**

```powershell
docker container run -it --name myvolumecontainer -v myvolume:/temp/ ubuntu
root@fab78eece7fd:/# echo hello, volume >> /temp/hello_volume
root@fab78eece7fd:/# exit
exit
```

**#3. 동일 볼륨을 사용하는 컨테이너를 추가로 실행**

```powershell
docker container run -it --name ourvolumecontainer -v myvolume:/temp/ ubuntu
root@3c575737fec4:/# ls /temp 
hello_volume      //#2에서 생성한 파일이 존재(공유)하는 것을 확인
root@3c575737fec4:/# cat /temp/hello_volume
hello, volume
```

**#4. docker inspect명령으로 볼륨의 저장 위치를 확인**

```powershell
docker volume inspect myvolume <= docker inspect --type volume myvolume 동일
[
    {
        "CreatedAt": "2023-09-26T02:25:02Z",
        "Driver": "local",
        "Labels": null,
        "Mountpoint": "/var/lib/docker/volumes/myvolume/_data",
        "Name": "myvolume",
        "Options": null,
        "Scope": "local"
    }
]
```

![image](https://github.com/Suah-Cho/STUDY/assets/102336763/fc15c960-c4e5-4ee0-81bb-d37d51fef4ae)


```powershell
docker container run -it --name myvolumecontainer -v newvolume:/root/ ubuntu
root@2437a72ffd60:/# echo hello, volume >> /root/hello_volume
root@2437a72ffd60:/# exit
exit

docker container run -it --name ourvolumecontainer -v myvolume:/temp/ ubuntu
root@e8607fead48a:/# ls /temp
hello_volume
root@e8607fead48a:/# cat /temp/hello_volume
hello, volume
hello, volume
root@e8607fead48a:/#

docker volume ls
DRIVER    VOLUME NAME
local     myvolume
local     newvolume
```

```powershell
docker container run -itd -v testvolume:/temp/ --name rwcontainer ubuntu
e046cc46e3f74a003304c37a8965ebf300534d0f291b6e0901c024a01a5c47ac

docker container run -itd -v testvolume:/temp/:ro --name rocontainer ubuntu
15e5db96cf434b2100ee68248327f31e0d0ac85ca364f3326e8f5fb72e94b82d

docker container exec -it rwcontainer /bin/bash => 읽기/쓰기 모두 가능
root@e046cc46e3f7:/# echo hello >> /temp/hello.txt
root@e046cc46e3f7:/# cat /temp/hello.txt
hello
root@e046cc46e3f7:/# exit
exit

docker container exec -it rocontainer /bin/bash => 읽기만 가능
root@15e5db96cf43:/# echo HI > /temp/hi.txt
bash: /temp/hi.txt: Read-only file system //read-only file system으로 작성이 불가하다.
root@15e5db96cf43:/# ls /temp
hello.txt
root@15e5db96cf43:/# cat /temp/hello.txt
hello
root@15e5db96cf43:/# exit
exit
```

### 컨테이너가 사용하고 있는 네트워크를 확인

```bash
docker container run -d --name my-todo-app myanjini/react-todo-app:v1

docker container inspect my-todo-app
"Networks": {
                "bridge": {
                    "IPAMConfig": null,
                    "Links": null,
                    "Aliases": null,
                    "NetworkID": "4719cad95f96a527d41c91d86a4766898272aec1b6de6da919746827a31d08bd",
                    "EndpointID": "e00687903e5efdeb10f14821cfab934920a74453e7783226da7875ff2fe3be93",
                    "Gateway": "172.17.0.1",
                    "IPAddress": "172.17.0.2",
                    "IPPrefixLen": 16,
                    "IPv6Gateway": "",
                    "GlobalIPv6Address": "",
                    "GlobalIPv6PrefixLen": 0,
                    "MacAddress": "02:42:ac:11:00:02",
                    "DriverOpts": null
                }
            }
```

**네트워크 생성**

```bash
docker network create --driver=bridge web-network
01f1333aed97755f9b17441a72c39de5ceef21f16935c04ed53e9c2d3f7b952a

docker network ls
NETWORK ID     NAME          DRIVER    SCOPE
4719cad95f96   bridge        bridge    local
cd05592bbaf8   host          host      local
3d5668cfa9eb   none          null      local
01f1333aed97   web-network   bridge    local
```

**네트워크 연결/연결 해제**

```bash
docker network connect web-network my-todo-app

docker container inspect my-todo-app
"Networks": {
                "bridge": {
                    "IPAMConfig": null,
                    "Links": null,
                    "Aliases": null,
                    "NetworkID": "4719cad95f96a527d41c91d86a4766898272aec1b6de6da919746827a31d08bd",
                    "EndpointID": "e00687903e5efdeb10f14821cfab934920a74453e7783226da7875ff2fe3be93",
                    "Gateway": "172.17.0.1",
                    "IPAddress": "172.17.0.2",
                    "IPPrefixLen": 16,
                    "IPv6Gateway": "",
                    "GlobalIPv6Address": "",
                    "GlobalIPv6PrefixLen": 0,
                    "MacAddress": "02:42:ac:11:00:02",
                    "DriverOpts": null
                },
                "web-network": {
                    "IPAMConfig": {},
                    "Links": null,
                    "Aliases": [
                        "2efbe7314595"
                    ],
                    "NetworkID": "01f1333aed97755f9b17441a72c39de5ceef21f16935c04ed53e9c2d3f7b952a",
                    "EndpointID": "a381290614aca9d5d9acbcc932d4e804a9b742c42fde71e86077b19227f3e129",
                    "Gateway": "172.18.0.1",
                    "IPAddress": "172.18.0.2",
                    "IPPrefixLen": 16,
                    "IPv6Gateway": "",
                    "GlobalIPv6Address": "",
                    "GlobalIPv6PrefixLen": 0,
                    "MacAddress": "02:42:ac:12:00:02",
                    "DriverOpts": {}
                }
```

**네트워크 상세 정보 확인**

```bash
docker network inspect web-network
[
    {
        "Name": "web-network",
        "Id": "01f1333aed97755f9b17441a72c39de5ceef21f16935c04ed53e9c2d3f7b952a",
        "Created": "2023-09-26T07:03:34.517603017Z",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": {},
            "Config": [
                {
                    "Subnet": "172.18.0.0/16",
                    "Gateway": "172.18.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {
            "2efbe73145958273aa8c6cac1cb10dcc32e881030fba9529fb0c3f02942a9927": {
                "Name": "my-todo-app",
                "EndpointID": "a381290614aca9d5d9acbcc932d4e804a9b742c42fde71e86077b19227f3e129",
                "MacAddress": "02:42:ac:12:00:02",
                "IPv4Address": "172.18.0.2/16",
                "IPv6Address": ""
            }
        },
        "Options": {},
        "Labels": {}
    }
]
```

**네트워크 삭제**

```bash
docker network rm web-network
Error response from daemon: error while removing network: network web-network id 01f1333aed97755f9b17441a72c39de5ceef21f16935c04ed53e9c2d3f7b952a has active endpoints
// 사용중인 컨테이너가 있어서 삭제 불가

docker network disconnect web-network my-todo-app
// 컨테이너랑 네트워크 disconnect(분리)

docker network rm web-network
web-network

docker network ls
NETWORK ID     NAME      DRIVER    SCOPE
4719cad95f96   bridge    bridge    local
cd05592bbaf8   host      host      local
3d5668cfa9eb   none      null      local
```

**컨테이너를 시작할 때 사용할 네트워크를 지정**

```bash
docker network create --driver=bridge mybridgenetwork
b5e13720a90140afd49a8e3cda6ef9f8197acd935a8c7b757dc7d76894589137

docker network ls
NETWORK ID     NAME              DRIVER    SCOPE
4719cad95f96   bridge            bridge    local
cd05592bbaf8   host              host      local
b5e13720a901   mybridgenetwork   bridge    local
3d5668cfa9eb   none              null      local

docker container run -d -p 80 --name my-todo-app-2 --net mybridgenetwork myanjini/react-todo-app:v1
2a237bcf01b47c63567af7c0556fd4ea7068fbb2a2f716e1e82872b6d5e52449
// 컨테이너 만들 때 네트워크 지정

docker container ls
CONTAINER ID   IMAGE                        COMMAND                   CREATED          STATUS          PORTS                   NAMES
438cf044dea2   myanjini/react-todo-app:v1   "/docker-entrypoint.…"   50 seconds ago   Up 49 seconds   0.0.0.0:59108->80/tcp   my-todo-app-2
a22f136c6a8e   myanjini/react-todo-app:v1   "/docker-entrypoint.…"   15 minutes ago   Up 15 minutes   80/tcp                  my-todo-app

docker container inspect my-todo-app-2

            "Networks": {
                "mybridgenetwork": {
                    "IPAMConfig": null,
                    "Links": null,
                    "Aliases": [
                        "438cf044dea2"
                    ],
                    "NetworkID": "14e9f2be902697a7f0d4cebcb135b78951983a44e7f7f27d74e5643795442d88",
                    "EndpointID": "643c1350906a7ee3a0811fc5092feea2f6c9d6d7af1a26bb2b474d03feda02f0",
                    "Gateway": "172.20.0.1",
                    "IPAddress": "172.20.0.2",
                    "IPPrefixLen": 16,
                    "IPv6Gateway": "",
                    "GlobalIPv6Address": "",
                    "GlobalIPv6PrefixLen": 0,
                    "MacAddress": "02:42:ac:14:00:02",
                    "DriverOpts": null
                }
            }
```

**centos 이미지를 이용해서 mycentos 이름의 컨테이너를 실행**

```bash
docker container run -itd --name mycentos centos

docker container ls
CONTAINER ID   IMAGE                        COMMAND                   CREATED              STATUS              PORTS                   NAMES
d9f5e238e05a   myanjini/react-todo-app:v1   "/docker-entrypoint.…"   36 seconds ago       Up 34 seconds       0.0.0.0:59135->80/tcp   my-todo-app-2
9ab6a5bb35eb   myanjini/react-todo-app:v1   "/docker-entrypoint.…"   46 seconds ago       Up 45 seconds       0.0.0.0:80->80/tcp      my-todo-app
74d0d80b2f97   centos                       "/bin/bash"               About a minute ago   Up About a minute                           mycentos
```

**my-todo-app, my-todo-app-2, mycentos 컨테이너가 사용하고 있는 네트워크 확인**

```bash
C:\docker> docker container inspect my-todo-app		⇐ 172.17.0.3/16 bridge
C:\docker> docker container inspect my-todo-app-2		⇐ 172.20.0.2/16 mybridgenetwork
C:\docker> docker container inspect mycentos		⇐ 172.17.0.2/16 bridge

// my-todo-app 컨테이너와 mycentos 컨테이너는 동일 네트워크(172.17 네트워크)를 사용하고 있음
```

```bash
// 파워쉘에서 포맷팅된 출력으로 확인이 가능
docker container inspect -f '{{range .NetworkSettings.Networks}}{{println .IPAddress}}{{println .NetworkID}}{{end}}' mycentos
172.17.0.2
5c25d796d992bffa6e8579fb619fd2a842bc548fabcd970ed9577d6b5584b19f
```

**mycentos 컨테이너를 my-todo-app-2컨테이너가 연결되어 있는 mybridgenetwork 네트워크로 연결**

```bash
docker network connect mybridgenetwork mycentos

docker container exec mycentos ping 172.20.0.2
PING 172.20.0.2 (172.20.0.2) 56(84) bytes of data.
64 bytes from 172.20.0.2: icmp_seq=1 ttl=64 time=0.060 ms
64 bytes from 172.20.0.2: icmp_seq=2 ttl=64 time=0.054 ms
64 bytes from 172.20.0.2: icmp_seq=3 ttl=64 time=0.087 ms		
// my-todo-app-2 컨테이너로 연결되는 것을 확인

docker container exec mycentos ping 172.17.0.3
PING 172.17.0.3 (172.17.0.3) 56(84) bytes of data.
64 bytes from 172.17.0.3: icmp_seq=1 ttl=64 time=0.050 ms
64 bytes from 172.17.0.3: icmp_seq=2 ttl=64 time=0.090 ms
64 bytes from 172.17.0.3: icmp_seq=3 ttl=64 time=0.093 ms
// my-todo-app 컨테이너로 연결되는 것을 확인
```

**mycentos 컨테이너의 네트워크 정보를 확인**

```bash
docker container inspect mycentos

            "Networks": {
                "bridge": {
                    "IPAMConfig": null,
                    "Links": null,
                    "Aliases": null,
                    "NetworkID": "5c25d796d992bffa6e8579fb619fd2a842bc548fabcd970ed9577d6b5584b19f",
                    "EndpointID": "e20c9d66dad4951fb03415a3eefbe3688081f11126c52a09ee2f260c896ec01b",
                    "Gateway": "172.17.0.1",
                    "IPAddress": "172.17.0.2",
                    "IPPrefixLen": 16,
                    "IPv6Gateway": "",
                    "GlobalIPv6Address": "",
                    "GlobalIPv6PrefixLen": 0,
                    "MacAddress": "02:42:ac:11:00:02",
                    "DriverOpts": null
                },
                "mybridgenetwork": {
                    "IPAMConfig": {},
                    "Links": null,
                    "Aliases": [
                        "74d0d80b2f97"
                    ],
                    "NetworkID": "14e9f2be902697a7f0d4cebcb135b78951983a44e7f7f27d74e5643795442d88",
                    "EndpointID": "eb5661f1cdefdc86aa035b1a421587ec19c49906ca228ed3ae230eeb2e5f1c2b",
                    "Gateway": "172.20.0.1",
                    "IPAddress": "172.20.0.3",
                    "IPPrefixLen": 16,
                    "IPv6Gateway": "",
                    "GlobalIPv6Address": "",
                    "GlobalIPv6PrefixLen": 0,
                    "MacAddress": "02:42:ac:14:00:03",
                    "DriverOpts": {}
                }
            }
```
