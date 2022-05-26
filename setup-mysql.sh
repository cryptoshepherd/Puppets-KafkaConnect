#!/bin/bash

docker exec -i mysql  mysql -u root -ptest < $PWD/connect-mysql.sql
