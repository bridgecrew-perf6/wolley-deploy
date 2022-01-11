FROM python:3.9.0

# 도커가 (혹은 portainer가) build 시 속도를 위해 caching을 해서,
# 장고에서 내용을 수정 후 다시 build할 때 마저도 cache하는 불상사가 없도록
# 아래의 명령어를 바꿔가면서 (예: testing!으로 했다가 test!!로 했다가 등등) build
RUN echo "WEWQEDADSting!!!"

RUN mkdir /root/.ssh/

ADD ./.ssh/id_rsa /root/.ssh/id_rsa

RUN chmod 600 /root/.ssh/id_rsa

RUN touch /root/.ssh/known_hosts

RUN ssh-keyscan github.com >> /root/.ssh/known_hosts


WORKDIR /home/alpha.technic/

# 한국 시간으로 설정
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul
RUN apt-get install -y tzdata

RUN git clone git@github.com:neo-wolley/wolley-deploy.git

WORKDIR /home/alpha.technic/wolley-deploy/

RUN pip install -r requirements.txt

RUN pip install gunicorn

RUN pip install mysqlclient

EXPOSE 8000

CMD ["bash", "-c", "python manage.py collectstatic --settings=myapi.settings.deploy --no-input && python manage.py migrate --settings=myapi.settings.deploy && gunicorn myapi.wsgi --env DJANGO_SETTINGS_MODULE=myapi.settings.deploy --bind 0.0.0.0:8000"]

# superuser 만드는 법
# pemkey 가지고 ubuntu 접속
# 장고 컨테이너에 접속 : sudo docker exec -it [컨테너 이름] /bin/bash
# 관리자 생성 : python manage.py createsuperuser --settings=BACKEND.settings.deploy이

# /home/alpha.technic 폴더에서 다음의 명령으로 이미지 빌드
# sudo docker image build -t django_image:1 .

