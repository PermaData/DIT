#!/bin/bash

echo "Grab rill zip file and unpack it. Using zip file so git is unnecessary."
wget https://github.com/PermaData/rill/archive/41cf89141dd3d78b6a67e26d4c67ffa93a03b8fb.zip
unzip *.zip
mv rill-*/* dit_flow/rill
rm -rf rill-*

echo "Download and install conda."
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
CONDA_PATH="$(pwd)/conda"
bash Miniconda3-latest-Linux-x86_64.sh -b -p $CONDA_PATH
export PATH=$CONDA_PATH/bin:$PATH
conda create -y -n dit_3 python=3.5
source activate dit_3
pip install -r dit_flow/requirements.txt

echo "Create environment setup script to run before using DIT."
ENV_SH="
echo 'Adding conda to your path...'
export PATH=$(CONDA_PATH)/bin:\$PATH
echo 'Activating dit_3 conda environment...'
source activate dit_3
echo 'All done. Enjoy!'"

echo "$ENV_SH" > env.sh

echo "Install dit_widget and rill python packages."
cd dit_flow
python setup.py
