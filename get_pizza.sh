#!/bin/bash
SESSION=$(bw unlock $1 | awk 'NR==4' | sed 's/^$ //')
$SESSION
echo "New Session has been created: $BW_SESSION"

activate() {
	. ./venv/bin/activate
	echo "Activated virtual env"
}

run_app() {
	python ./app/run.py
}

activate
run_app
