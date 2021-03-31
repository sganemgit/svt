#!/bin/bash

# @author Shady Ganem <shady.ganem@intel.com>

echo -e "Input args: $@"
echo -e "\nInstalling Depedencies\n"
sudo yum -y install python3 python2
python3 -m ensurepip
yum -y install python-pip
pip3 install -r $PWD/core/depend/requirements.txt
pip install -r $PWD/core/depend/requirements.txt


if [[ -n "$1" ]]
then 
	echo -e "in if"
	if [[ "$1" -eq "pythonsv" ]]
	then 
		if [[ "$2" -eq "mev" ]]
		then
			sudo python3 -m pip install mtevans --upgrade -i https://ubit-artifactory-or.intel.com/artifactory/api/pypi/DSD-SD-SV-Tools-pypi-local/simple --user
			sudo python3 -m mtevans.update_tools
			sudo python3 -m mtevans.getdefs

		fi
	fi
fi

if [[ -z PYTHONPATH ]]
then
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
echo -e "\nDone\n"
