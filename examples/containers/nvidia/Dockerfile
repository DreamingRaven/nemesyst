FROM archlinux:latest

ARG user_name=archie

ARG user_password=archer

ARG branch=master

RUN pacman -Syyuu sudo nvidia git base-devel --noconfirm && \
    useradd -m -p $(openssl passwd -1 ${user_password}) ${user_name} && \
    echo "${user_name} ALL=(ALL) ALL" >> /etc/sudoers

RUN pacman -S python python-pip pyalpm --noconfirm
    # pip install "git+https://github.com/DreamingRaven/nemesyst.git#branch=${branch}"

USER ${user_name}

RUN mkdir ~/git && \
    cd ~/git && \
    git clone "https://aur.archlinux.org/pikaur.git" && \
    cd ~/git/pikaur && \
    echo "${user_password}" | makepkg -S -si --noconfirm && \
    cd ~/git && \
    git clone "https://github.com/DreamingRaven/nemesyst" && \
    cd ~/git/nemesyst && \
    git checkout ${branch} && \
    cd ~/git && \
    echo "${user_password}" | sudo -S -v
