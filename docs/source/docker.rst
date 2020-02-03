.. _dockerfile: https://docs.docker.com/engine/reference/builder/
.. |dockerfile| replace:: Dockerfile

.. _bash shell: https://en.wikipedia.org/wiki/Bash_%28Unix_shell%29
.. |bash shell| replace:: Bash shell

.. _docker: https://www.docker.com/
.. |docker| replace:: Docker

.. |dockerisation| replace:: :ref:`section_docker`

.. _section_docker:

Dockerisation
=============

Docker is a lightweight semi-vm that can help automate reproducibility, dependency management, deployment, and use of some code which is containerized.
Considering the relative ease with which Docker is used, modified/adjusted, with only a minimal amount of code, it has quite a profound affect on work-flows, making really nightmarish scenarios much easier to handle.

For docker installation you may need to look up instructions online but after installing docker (minimum version 19.03) and nvidia container toolkit, you will need not install anything further, and can instead rely on the Dockerfile and docker to install and manage dependencies from then on. If you would like more automation/ to use docker-compose then please ensure you also have docker-compose installed.

There are two available versions of our Dockerfile:

- Archlinux based nemesyst docker ``examples/containers/nemesyst/Dockerfile``; This docker is the one we seek to support since it will force us to stay up to date with the latest software and changes so we never end up in a crippling dependency requirement. It should be noted however that it is not quite complete.
- Ubuntu based nemesyst docker ``examples/containers/nemesyst_ubuntu/Dockerfile``; This docker is the one we make available for the purposes of longer term support, and for those that just prefer Ubuntu (you must be crazy!). This one is the more supported by depended on projects such as tf-seal so is easier to maintain.

Docker Usage (Linux)
********************

While docker is very portable to most platforms, we do not maintain any non-x86_64, Microsoft Windows or Mac systems, thus we cannot presume to give sound Docker usage on these other platforms. However the usage should largely remain the same, but presumably without the need for privilege escalation using sudo for Win and Mac.

Using docker usually revolves around only two steps building the image you would like to use, and then using it either interactively or by issuing explicit commands to be executed. First however we should briefly mention the two most important files related to this a .dockerignore file, and a |dockerfile|_ .

|dockerfile|_
+++++++++++++

A |dockerfile|_ is a short command based script that defines how to create a container. These can and usually are built on other containers. Please refer to the |dockerfile|_ documentation for a more in depth breakdown.

:|Dockerfile|_ example ``examples/containers/nemesyst_ubuntu/Dockerfile``:

  .. literalinclude:: ../../examples/containers/nemesyst_ubuntu/Dockerfile

.dockerignore
+++++++++++++

A .dockerignore is similar in function to a .gitignore and supports similar syntax. Special care should be paid to .dockerignore files as they are both useful to minimise the risk of potential secrets being leaked into a container, their container size etc, but they can also cause problems with things like the ```COPY``` command leading to unexpected results. We personally recommend a whitelist strategy .dockerignore where you specify only what you would like to be copied in.

:whitelist .dockerignore example ``examples/containers/nemesyst_ubuntu/.dockerignore``:

  .. literalinclude:: ../../examples/containers/nemesyst_ubuntu/.dockerignore

Building
++++++++

With a |dockerfile|_ in the current directory to build a dockerfile into a docker image:

:|bash shell|_ creating a tagged docker image:

    .. parsed-literal::

        sudo docker build -t example/nemesyst .

This tag "example/nemesyst" will help you reference the docker image later on, like easy removal, and general use.

Running
+++++++

When we take a built image and run it, it is now called a container. Images are the immutable snapshots that you have built, containers are the changed containers for all the work that has happened since being an image.

To create a container from an image/ to run a docker image you can either:

:|bash shell|_ creating/running a CPU only container from a tagged ("example/nemesyst") docker image:

    .. parsed-literal::

        sudo docker run -it example/nemesyst bash

or

:|bash shell|_ creating/running a GPU enabled container ("example/nemesyst"):

    .. parsed-literal::

        sudo docker run --gpus all -it example/nemesyst bash

Cleaning up/ Removing
+++++++++++++++++++++

It may be necessary over the course of any experimentation or creation to occasionally clean up any images and containers that may still be taking up space on your system.

:|bash shell|_ removing/ pruning everything:

    .. parsed-literal::

        sudo docker system prune

:|bash shell|_ removing all images:

    .. parsed-literal::

        sudo docker rmi -f $(sudo docker images -q)

:|bash shell|_ removing all containers:

    .. parsed-literal::

        sudo docker rm (sudo docker ps -a -q)
