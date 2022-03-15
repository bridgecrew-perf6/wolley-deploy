# Wolley

- **위치를 바탕으로 AI가 하루를 기록하고, 새로운 플레이스를 추천하는 서비스**
- **untinkable question : AI가 내 삶을 기록하고 개선 시켜 줄 수 있을까?**



## Environment

![https://user-images.githubusercontent.com/58129950/155041694-57af051c-bd65-4afc-b232-b930fa7039f7.png](https://user-images.githubusercontent.com/58129950/155041694-57af051c-bd65-4afc-b232-b930fa7039f7.png)

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



## Prerequisite

- Make a virtual environment

  ```shell
  $ cd server
  $ python3 -m venv myvenv
  ```

- Run a virtual environment

  ```shell
  (myvenv) ~/wolley-deploy$ source myvenv\Scripts\activate
  ```

- Install requirements

  - install requirements

    ```shell
    (myvenv) ~$ pip install -r requirements.txt
    ```

  - pip upgrade

    ```shell
    (myvenv) ~$ python3 -m pip install --upgrade pip
    ```

    

## Usage

```
(myvenv) ~/wolley-deploy$ python manage.py makemigrations
(myvenv) ~/wolley-deploy$ python manage.py migrate
```

```shell
(myvenv) ~/wolley-deploy$ python manage.py runserver
```



## Service Description

![PJ_SUMMARY](./_project_review/PJ_SUMMARY.png)
