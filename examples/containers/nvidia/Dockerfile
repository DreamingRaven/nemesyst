FROM archlinux:latest
RUN pacman -Syyuu --noconfirm && \
    useradd -m -p $(openssl passwd -1 archer) archie
RUN pacman -S nvidia python python-pip base-devel --noconfirm \
    pip install "git+https://github.com/DreamingRaven/nemesyst.git#branch=master"
