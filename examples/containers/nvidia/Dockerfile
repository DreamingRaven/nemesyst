FROM archlinux:latest

# variable for user username to use in the container
ARG user_name=archie

# variable for user password to use in the container
ARG user_password=archer

# variable for which branch to use of nemesyst when installing it
ARG branch=master

# creating basic gpu capable archlinux system
RUN pacman -Syyuu sudo nvidia git base-devel python python-pip pyalpm --noconfirm

#
RUN useradd -m -p $(openssl passwd -1 ${user_password}) ${user_name} && \
    echo "${user_name} ALL=(ALL) NOPASSWD:/usr/bin/pacman" >> /etc/sudoers

# swapping to our newly created user
USER ${user_name}

# clone, build, and install pikaur
RUN mkdir ~/git && \
    cd ~/git && \
    git clone "https://aur.archlinux.org/pikaur.git" && \
    cd ~/git/pikaur && \
    makepkg -s --noconfirm && \
    echo "${user_password}" | sudo -S pacman -U *pkg.tar.xz --noconfirm

# clone, swap to desired branch, of nemesyst
RUN cd ~/git && \
    git clone "https://github.com/DreamingRaven/nemesyst" && \
    cd ~/git/nemesyst && \
    git checkout ${branch}

USER root

# attempt to install any package in our case python-tensorflow-cuda
RUN sudo -u ${user_name} pikaur -S --noconfirm python-tensorflow-cuda
