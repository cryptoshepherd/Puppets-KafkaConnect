FROM python:3.9
COPY ./requirements.txt /code/requirements.txt

WORKDIR /code

ENV http_proxy "http://proxy-muc.sky.de:8080"
ENV https_proxy "http://proxy-muc.sky.de:8080"
ENV PYTHONWARNINGS "ignore:Unverified HTTPS request"

RUN pip install -r requirements.txt

COPY . /code

CMD ["python", "./app.py" ]

# docker build -t flask_docker .
# docker run -d -p 5000:5000 flask_docker
