#!/bin/bash

sudo yum -y install python3
python3 -m ensurepip
pip3 install -r $PWD/core/depend/requirements.txt

if [[ -z PYTHONPATH ]]; then
	EXPORT_CMD='export PYTHONPATH='$PWD
	echo ${EXPORT_CMD} >> ~/.bashrc
	. ~/.bashrc
else 
	if [[ $PYTHONPATH == *'svt'* ]]; then
		echo -e "PYTHONPATH OK"
	else
		EXPORT_CMD='export PYTHONPATH=$PYTHONPATH:'$PWD
		echo ${EXPORT_CMD} >> ~/.bashrc
		. ~/.bashrc
	fi
fi
echo -e "Done"
