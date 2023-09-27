### flask app을 docker compose하여 부하 분산하기
**요구조건**
#### /whoareyou 접속하면 현재 서버의 주소를 출력하도록 소스 코드를 수정한 후 도커 이미지로 만들고, 
#### 이미지를 Docker Compose를 이용해서 동일한 컨테이너를 여러 개 실행 후 
#### http://localhost/whoareyou로 접속했을 때 컨테이너의 주소가 라운드 로빈되어서 출력하도록 하자.

**과정**
```powershell
docker image build -t myflask:3.0

docker-compose up -d --scale myflask=3
```

**실행 결과**
- 첫 화면
  ![image](https://github.com/Suah-Cho/STUDY/assets/102336763/8e6efb74-89a0-4801-bb74-fc8046f37b69)
- /whoareyou
  ![image](https://github.com/Suah-Cho/STUDY/assets/102336763/5e1e0f7b-19f9-47ef-961c-c2f1c2d6d778)
  ![image](https://github.com/Suah-Cho/STUDY/assets/102336763/7fe635fc-d1f7-45f0-84d7-303bb49249f0)
  ![image](https://github.com/Suah-Cho/STUDY/assets/102336763/99d38b0f-dd67-4a24-a730-9fc8fab7dc10)
