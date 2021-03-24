#!/bin/bash

sudo pip install -r $PWD/core/depend/requirements.txt

if [[ -z PYTHONPATH ]]; then
	EXPORT_CMD='export PYTHONPATH='$PWD
	echo ${EXPORT_CMD} >> ~/.bashrc
	source ~/.bashrc
else 
	if [[ $PYTHONPATH == *'svt'* ]]; then
		echo -e "PYTHONPATH OK"
	else
		export PYTHONPATH=PYTHONPATH:$PWD
		EXPORT_CMD='export PYTHONPATH=$PYTHONPATH:'$PWD
		echo ${EXPORT_CMD} >> ~/.bashrc
		source ~/.bashrc
	fi
fi
echo -e "Done"
