#!/bin/bash

echo Clean zk-data
rm -rf  $PWD/vol1/zk-data/*
echo Clean zk-txn-logs
rm -rf $PWD/vol2/zk-txn-logs/*
echo Clean kafka-data
rm -rf $PWD/vol3/kafka-data/*
rm -rf $PWD/vol4/kafka-data/*
rm -rf $PWD/vol5/kafka-data/*
echo Clean Mysql DB
rm -rf $PWD/mysql/*
echo Prune containers
docker container prune
