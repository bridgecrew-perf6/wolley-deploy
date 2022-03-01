## PJ 회고

- 반성
  - 무중단배포 못함
    - 블루그린까지는 아니더라도, Rolling 정도는 구축했어야 했다.
    - hostPC에 nginx(로드밸런서)를 두고, django 컨테이너, mariadb 컨테이너만 docker로 관리하면서 stack을 2개 쯤 만드는 방향으로 무중단 배포를 하고 싶다.
  - Start Up Script 활용
    - `Dockerfile`, `docker-compose.yml`을 활용해서 비교적 쉽게 서비스를 업데이트할 수 있기는 했다. 
    - 그러나, 위 2개 파일을 이용해서 하는 반복적인 작업을 모두 Start up script에 적어두었다면, instance를 restart하는 것만으로도 손쉬운 배포가 가능했을 듯 하다.
  - DB의 철학 vs Docker의 철학
    - 손쉬운 접근과 잦은 수정과 삭제를 위해 DB를 Docker container로 구성하였는데, 이 둘의 철학이 충돌한다고 느낌	
    - DB : 영속적인 데이터 보관을 위함
    - Docker : 쉽게 띄우고 쉽게 삭제하고, 쉬운 수정과 삭제를 위함
    - DB의 구조에 대한 업데이트가 소극적이게 되는 시점에 클라우드에서 제공하는 DB로 옮겨가는 방향으로 하고 싶다.
  - GPS로그 -> 파이차트 Test 환경
    - 서비스의 핵심이 되는 메인 로직에 대한 TEST 환경은 sprint 초반에 작성할 것.
    - 이렇게 공수가 크고 어려운 작업일 줄 예상하지 못한 것이 패착
    - 그럼에도 불구하고, 서비스의 메인 로직이라면 필히 test환경을 발빠르게 만들었어야.
  
- My Skill Up
  - stay point detection 알고리즘
  - docker
    - docker의 이미지 구조, 동작
    - Dockerfile 작성
    - docker-compose.yml 파일 작성
  - jenkins (CICD)
  - linux service
  - test 코드 작성
    - test 코드에 파라미터를 전달하는 방법
  - swagger
    - swagger로 API 명세 작성
  - nGrinder
    - 부하테스트 환경 구축
  - python logger
  - python folium (GPSLog 시각화 프레임웤)
  - FCM을 통한 (silent) push notification 방법
  - 메세지큐

