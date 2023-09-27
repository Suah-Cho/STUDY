/whoareyou 접속하면 현재 서버의 주소를 출력하도록 소스 코드를 수정한 후 도커 이미지로 만들고, 
이미지를 Docker Compose를 이용해서 동일한 컨테이너를 여러 개 실행 후 
http://localhost/whoareyou로 접속했을 때 컨테이너의 주소가 라운드 로빈되어서 출력되는 것을 확인해 보세요.
