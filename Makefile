SMARTCAN_HOME=$(shell pwd)
PIP=${SMARTCAN_HOME}/venv/bin/pip
PYTHON=${SMARTCAN_HOME}/venv/bin/python

setup:
	if [ ! -d "./venv" ]; then $(shell which python3) -m venv venv; fi

build-pi: setup
	${PIP} install -r requirements-raspi.txt

build-dev: setup
	${PIP} install -r requirements-dev.txt

run:
	${PYTHON} embedded.py

startup-add:
	sudo ln -s ${SMARTCAN_HOME}/bin/smartcan.sh /etc/init.d/smartcan
	sudo update-rc.d smartcan defaults

startup-remove:
	sudo update-rc.d -f smartcan remove
	sudo rm -f /etc/init.d/smartcan