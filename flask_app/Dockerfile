FROM python:3.9
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

#ENV http_proxy ""
#ENV https_proxy ""
#ENV PYTHONWARNINGS "ignore:Unverified HTTPS request"
COPY . /code
CMD ["python", "app.py" ]

# docker build -t flask_docker .
# docker run -d -p 5000:5000 flask_docker
