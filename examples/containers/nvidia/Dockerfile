FROM archlinux:latest

# variable for user username to use in the container
ARG user_name=archie

# variable for user password to use in the container
ARG user_password=archer

# variable for which branch to use of nemesyst when installing it
ARG branch=master

# creating basic gpu capable archlinux system with user
RUN pacman -Syyuu sudo nvidia git base-devel --noconfirm && \
    useradd -m -p $(openssl passwd -1 ${user_password}) ${user_name} && \
    echo "${user_name} ALL=(ALL) ALL" >> /etc/sudoers

# creating specific python system
RUN pacman -S python python-pip pyalpm --noconfirm

# swapping to our newly created user
USER ${user_name}

# clone and build pikaur as well as cloning nemesyst for development
RUN mkdir ~/git && \
    cd ~/git && \
    git clone "https://aur.archlinux.org/pikaur.git" && \
    cd ~/git/pikaur && \
    echo "${user_password}" | makepkg -S -si --noconfirm && \
    cd ~/git && \
    git clone "https://github.com/DreamingRaven/nemesyst" && \
    cd ~/git/nemesyst && \
    git checkout ${branch} && \
    cd ~/git

# echo "${user_password}" | sudo -S -v
