#!/bin/bash

# @author Shady Ganem <shady.ganem@intel.com>
set -e
echo -e "Input args: $@"

if [[ "$1" -eq "intec" ]]
then 
	#sudo dnf config-manager --add-repo https://dl.winehq.org/wine-builds/fedora/30/winehq.repo	
	#sudo dnf -y install winehq-stable
	echo -e ""
fi

if [[ "$1" == "openipc" ]]
then
	if [[ ! -d ~/bin/openIPC ]]
	then
		echo -e "Making Directory $HOME/bin/openIPC"
		mkdir -p ~/bin/openIPC
		
		read -p "Username: " USERNAME
		read -s -p "Password: " PASSWORD
		ARTIFACT=OpenIPCDebugLibrary.StandaloneLinux.1.2106.5146.600.x64.tar.gz
		curl -u $USERNAME:$PASSWORD https://ubit-artifactory-or.intel.com/artifactory/list/dsdjf-pvt-repo/OpenIPC/2109/Linux/OpenIPCDebugLibrary.StandaloneLinux.1.2106.5146.600.x64.tar.gz -o $HOME/bin/$ARTIFACT
		tar -C $HOME/bin/openIPC -xf $HOME/bin/$ARTIFACT 
		rm -rf $HOME/bin/$ARTIFACT
	else
		echo -e "openIPC already installed at $HOME/bin/openIPC"
	fi
fi

if [[ "$1" == "pythonsv" ]]
then 
	if [[ "$2" -eq "mev" ]]
	then
		python3 -m pip install mtevans --upgrade -i https://ubit-artifactory-or.intel.com/artifactory/api/pypi/DSD-SD-SV-Tools-pypi-local/simple --user
		python3 -m mtevans.update_tools
		python3 -m mtevans.getdefs
		rm -rf update_tools_logs namednodes.log
	fi
fi

if [[ "$1" == "" ]]
then
	echo -e "\nInstalling Depedencies\n"
	sudo yum -y install python3 python2
	sudo yum -y install python-pip
	sudo yum -y install python3-pip
	sudo python3 -m pip install -U pip
	sudo yum -y install python3-pip
	python3 -m ensurepip
	pip3 install -r $PWD/core/depend/requirements.txt
	pip install -r $PWD/core/depend/requirements.txt
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
fi
echo -e "\nDone\n"
