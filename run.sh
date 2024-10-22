#!/usr/bin/bash

venvpath=.venv/bin/activate


echo $(command -v python3)
echo $(command -v pip3)

if [ ! -d .venv ]
then
	echo "Creating virtual environment..."
	python3 -m venv .venv
fi

if [ -f "$venvpath" ]; then
	echo "Activating virtual envorinment..."
	source $venvpath
else
	echo "Error: Unable to find $venvpath"
	exit 1
fi

which python3

if command -v pip3 > /dev/null; then
	echo "Installing dependencies..."
	pip3 install -r requirements.lock
else
	echo "Error: pip3 not found"
	exit 1
fi

export PYTHONPATH=$(pwd)

echo "Running app..."

python3 app/run.py
