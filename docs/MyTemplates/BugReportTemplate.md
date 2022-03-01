<!--
Issue Guide

- 적절한 제목으로 변경해주세요. (ex: [Bug Report] 동선 잔상, 그려지다 마는 현상)
- 최대한 아래 템플릿의 모든 칸을 채워주세요.
- 적절한 Label을 달아주세요.
- 담당자가 모호하거나 담당자를 모르는 경우, assign 칸을 비워주세요.
- 담당자가 확실한 경우 assign에 담당자를 언급해주세요.
- 담당자는 확인 후 라벨 P1-P3로 중요도를 표시해주세요.
- 담당자는 버그 수정 후 comment에 반영 예상 앱 버전을 남겨주세요.
-->

## 환경

![image](https://user-images.githubusercontent.com/58129950/155041694-57af051c-bd65-4afc-b232-b930fa7039f7.png)

- GCP setting

  - region : 오사카
  - 삭제 보호 : 설정됨
  - 부팅디스크
    - 운영체제 : ubuntu
  - 방화벽 : HTTP 트래픽
  - 고정 IP
  - port opened
    - 22, 80, 443, 8000, 8080, 8888, 9000
  - https 인증

- 도커 version 3.7

  - django-gunicorn 컨테이너 (custom image 기반)
  - nginx 1.19.5 컨테이너
  - mariadb 10.5 컨테이너

  



## 문제 상황 (기댓값 vs 실젯값)

**[기댓값]**

- 

**[실젯값]**

- 

**[Error Log]**

```shell
(paste here)
```



## 문제 원인 추정

- 

## 실제 문제 원인

- 



## Trial

- 

=> 결과 : **fail**



- 


=> 결과 : **성공**

## 해결 여부

- [] 해결 완료
- [x] 해결 중