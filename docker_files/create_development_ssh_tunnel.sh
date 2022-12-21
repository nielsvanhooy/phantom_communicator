#!/bin/bash

echo $APPLICATION_RUN_TYPE;

if [ "$APPLICATION_RUN_TYPE" == "development" ]; then
  echo "Creating development tunnel"
  mkdir /root/.ssh
  cp /data/application/docker/.ssh/id_rsa_jumpuser_rufus /root/.ssh/id_rsa_jumpuser_rufus
  cp /data/application/docker/development_ssh_config /root/.ssh/config

  chmod 400 /root/.ssh/id_rsa_jumpuser_rufus
  chmod 600 /root/.ssh/config
fi
