FROM archlinux:latest

ARG user_name=archie

ARG user_password=archer

RUN pacman -Syyuu sudo nvidia git --noconfirm && \
    useradd -m -p $(openssl passwd -1 ${user_password}) ${user_name} && \
    echo "${user_name} ALL=(ALL) ALL" >> /etc/sudoers

RUN pacman -S python python-pip --noconfirm && \
    pip install "git+https://github.com/DreamingRaven/nemesyst.git#branch=master"
