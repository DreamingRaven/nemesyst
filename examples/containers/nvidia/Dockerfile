FROM archlinux:latest

# variable for user username to use in the container
ARG user_name=archie

# variable for user password to use in the container
ARG user_password=archer

# variable for which branch to use of nemesyst when installing it
ARG branch=master

# creating basic gpu capable archlinux system
RUN pacman -Syyuu sudo nvidia git base-devel python python-pip pyalpm --noconfirm

# creating user with the desired permissions (NOPASS required for pikaur stages)
RUN useradd -m -p $(openssl passwd -1 ${user_password}) ${user_name} && \
    echo "${user_name} ALL=(ALL) NOPASSWD:/usr/bin/pacman" >> /etc/sudoers

# swapping to our newly created user
USER ${user_name}

# clone, build, and install pikaur
RUN mkdir /home/${user_name}/git && \
    cd /home/${user_name}/git && \
    git clone "https://github.com/actionless/pikaur" && \
    cd /home/${user_name}/git/pikaur && \
    makepkg -s --noconfirm && \
    echo "${user_password}" | sudo -S pacman -U *pkg.tar.xz --noconfirm

# swapping back to root to continue since we no longer desire to be a user for makepkg
USER root

# install more specific packages from community and AUR as needed
RUN sudo -u ${user_name} pikaur -S --noconfirm python-tensorflow-cuda

# changing to final user in case interactivity is desired
USER ${user_name}

# clone and checkout nemesyst
RUN cd ~/git && \
    git clone "https://github.com/DreamingRaven/nemesyst" && \
    cd ~/git/nemesyst && \
    git checkout ${branch}
