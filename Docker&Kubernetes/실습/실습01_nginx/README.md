### 실습01
#### nginx 이미지를 이용해서 본인만의 웹 서버 이미지를 작성하고, 작성한 이미지를 도커 허브에 등록해 보세요.

1. 생성할 이미지 이름은 mywebserver 로 설정
2. 컨테이너 실행 후 http://localhost:HOST_PORT/ 로 접속했을 때 아래와 같은 결과(화면)가 출력되어야 함
![image](https://github.com/Suah-Cho/STUDY/assets/102336763/ebfa7c8f-fde8-4131-a351-0fe7759fdb74)

3. nginx의 기본 웹 루트 디렉터리는 /usr/share/nginx/html 이며, 기본 페이지는 index.html 임

실행 예)  
c:\docker> docker container run -d -p 8888:80 --name mywebserver myanjini/mywebserver:v2  
Unable to find image 'myanjini/mywebserver:v2' locally  
v2: Pulling from myanjini/mywebserver  
3f9582a2cbe7: Pull complete  
9a8c6f286718: Pull complete  
e81b85700bc2: Pull complete  
73ae4d451120: Pull complete  
6058e3569a68: Pull complete  
3a1b8f201356: Pull complete  
b9ce3d43f311: Pull complete  
Digest: sha256:ce6199f052475c6d248e6b4804c14cacfad654bfb52696c2789c13f25e99498f  
Status: Downloaded newer image for myanjini/mywebserver:v2  
6854e77340c54dc2da5b36dabe5ac27cf39c126a298639583c9cef63886d071d  
