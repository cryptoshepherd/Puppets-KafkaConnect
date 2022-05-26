#!/bin/bash

echo Create zk-data
mkdir -p $PWD/vol1/zk-data
echo Create zk-txn-logs
mkdir -p $PWD/vol2/zk-txn-logs
echo Create kafka-data 1
mkdir -p $PWD/vol3/kafka-data
echo Create kafka-data 2
mkdir -p $PWD/vol4/kafka-data
echo Create kafka-data 1
mkdir -p $PWD/vol5/kafka-data
echo Create Mysql data dir
mkdir $PWD/mysql

echo Grant permissions

chown -R 1000:1000 $PWD/vol1/zk-data
chown -R 1000:1000 $PWD/vol2/zk-txn-logs
chown -R 1000:1000 $PWD/vol3/kafka-data
chown -R 1000:1000 $PWD/vol4/kafka-data
chown -R 1000:1000 $PWD/vol5/kafka-data
