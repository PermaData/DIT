#!/bin/bash

echo "Grab DIT zip file and unpack it. Using zip file so git is unnecessary."
# curl -L https://github.com/PermaData/DIT/archive/master.zip > dit.zip
curl -L https://github.com/PermaData/DIT/archive/widget_work.zip > dit.zip
unzip dit.zip
cd DIT-widget_work

echo "Download and install conda."
curl -L https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh > miniconda.sh
CONDA_PATH="$(pwd)/conda"
bash miniconda.sh -b -p $CONDA_PATH
rm miniconda.sh

export PATH=$CONDA_PATH/bin:$PATH
conda env create -f environment.yml
source activate dit

echo "Create environment setup script to run before using DIT."
ENV_SH="
echo 'Adding conda to your path...'
export PATH=$(pwd)/conda/bin:\$PATH
echo 'Activating dit conda environment...'
source activate dit
echo 'All done. Enjoy!'"

echo "$ENV_SH" > env.sh
