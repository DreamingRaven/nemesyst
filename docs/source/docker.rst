dockerisation
=============

Archlinux GPU tensorflow
++++++++++++++++++++++++

You will need to make sure the NVIDIA-container-toolkit is installed on arch using pikaur (and AUR helper) this is via:

pikaur -S nvidia-container-toolkit

This will check that the drivers are all working:

docker run --gpus all --rm nvidia/cuda nvidia-smi

Installing TensorFlow in a container using devel, and GPU support:

sudo docker pull tensorflow/tensorflow:devel-gpu
