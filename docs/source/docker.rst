dockerisation
=============

Archlinux GPU tensorflow
++++++++++++++++++++++++

You will need to make sure the NVIDIA-container-toolkit is installed on arch using pikaur (and AUR helper) this is via:

.. parsed-literal::

  pikaur -S nvidia-container-toolkit

Restart the docker daemon to ensure the NVIDIA toolkit is being used:

.. parsed-literal::

    systemctl restart docker

This will check that the drivers are all working:

.. parsed-literal::

  docker run --gpus all --rm nvidia/cuda nvidia-smi

Installing TensorFlow in a container using devel, and GPU support:

.. parsed-literal::

  docker pull tensorflow/tensorflow:devel-gpu-py3

Running the tensorflow container:

.. parsed-literal::

    docker run --gpus all -it tensorflow/tensorflow:devel-gpu-py3 bash
