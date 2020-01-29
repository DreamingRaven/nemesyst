.. _dockerfile: https://docs.docker.com/engine/reference/builder/
.. |dockerfile| replace:: Dockerfile

Dockerisation
=============

Docker is a lightweight semi-vm that can help automate reproducibility, dependency management, deployment, and use of some code which is containerized.
Considering the relative ease with which Docker is used, modified/adjusted, with only a minimal amount of code, it has quite a profound affect on work-flows, making really nightmarish scenarios much easier to handle.

For docker installation you may need to look up instructions online but after installing docker and nvidia container toolkit, you will need not install anything further, and can instead rely on the Dockerfile and docker to install and manage dependencies from then on. If you would like more automation/ to use docker-compose then please ensure you also have docker-compose installed.

There are two avaliable versions of our Dockerfile:

- Archlinux based nemesyst docker ``examples/containers/nemesyst/Dockerfile``; This docker is the one we seek to support since it will force us to stay up to date with the latest software and changes so we never end up in a crippling dependency requirement. It should be noted however that it is not quite complete.
- Ubuntu based nemesyst docker ``examples/containers/nemesyst_ubuntu/Dockerfile``; This docker is the one we make available for the purposes of longer term support, and for those that just prefer Ubuntu (you must be crazy!). This one is the more supported by depended on projects such as tf-seal so is easier to maintain.

Docker Usage (Linux)
********************

While docker is very portable to most platforms, we do not maintain any Microsoft Windows or Mac systems, thus we cannot presume to give sound Docker usage on these other platforms. However the usage should largely remain the same, but presumably without the need for privilege escalation using sudo.

|dockerfile|_
+++++++++++++

A |dockerfile|_ is a short command based script that defines how to create a container. These can and usually are built on other containers. Please refer to the |dockerfile|_ documentation for a more in depth breakdown.

:|Dockerfile|_ example ``examples/containers/nemesyst_ubuntu/Dockerfile``:

  .. literalinclude:: ../../examples/containers/nemesyst_ubuntu/Dockerfile

.dockerignore
+++++++++++++

A .dockerignore is similar in function to a .gitignore and supports similar syntax. Special care should be paid to .dockerignore files as they are both usefull to minimise the risk of potential secrets being leaked into a container, their container size etc, but they can also cause problems with things like the ```COPY``` command leading to unexpected results. We personally recommend a whitelist strategy .dockerignore where you specify only what you would like to be copied in.

:whitelist .dockerignore example ``examples/containers/nemesyst_ubuntu/.dockerignore``:

  .. literalinclude:: ../../examples/containers/nemesyst_ubuntu/.dockerignore

Building
++++++++

Running
+++++++

Archlinux GPU tensorflow
************************

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
