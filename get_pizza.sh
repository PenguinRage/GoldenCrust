#!/bin/bash
activate() {
	. ./venv/bin/activate
	echo "Activated virtual env"
}

run_app() {
	python ./app/run.py
}

activate
run_app
