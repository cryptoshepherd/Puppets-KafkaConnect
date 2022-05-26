<h1 align="center">
  <br>
  Kafka Connect Flask
  <br>
</h1>

![kcf](puppet.png)

<h4 align="center">A Minimal Flask Webapp for Kafka Connect</h4>



<p align="center">
  <a href="#key-features">Important Notes </a> •
  <a href="#key-features">How to test </a> •
  <a href="#key-features">Key Features</a> •
  <a href="#credits">To do</a> •
  <a href="#license">License</a>
</p>

## Important Notes

The graphical interface is pretty minimalistic. you can add a connector by passing the connector's name, 
the worker FQDN or IP and the REST API port. Your connector will be added to the database and you will be
ready to manage it. Right now you can:

1) Connector's and tasks status
2) Configuration download
3) Stop
4) Pause
5) Resume
6) Update config
7) Delete a connector

## How to test

Along with the repo, there are several scripts and a docker-compose.yml file which will allow you to quickly
speed up a mini local kafka cluster with a mysql db and an example source connector you can deploy to test
locally the web app. In order:

```bash
$ sudo sh setup.sh
$ docker-compose up -d

Wait a couple of minutes ...

$ docker ps 

Double check that broker1,2,3 connect and mysql are up and running

$ sh setup-mysql.sh
$ sh setup-topics.sh
```

in case of troubles with the containers, start from scratch with a clean situation by running the clean.sh script

```bash
$ sudo clean.sh
```

You can run the webapp locally first and build your image afterwards:

```bash
$ python flask_app/app.py
```


## Key Features

* Minimal Web Interface
* Basic Kconnect management with no need of 3th party tools or Kconnect REST
* Fully portable thanks to docker (On K8s as well)


## To do

* Implement basic auth
* Creation of a new connector from the web interface
* Implement SSL support
* Add schema Reg to the docker-compose



## License

MIT

---

> GitHub [@cryptoshepherd](https://github.com/) &nbsp;&middot;&nbsp;
> Twitter [@the_lello](https://twitter.com/)

