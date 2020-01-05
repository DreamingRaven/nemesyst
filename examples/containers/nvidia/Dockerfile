FROM archlinux:latest

RUN pacman -Syyuu sudo nvidia git --noconfirm && \
    useradd -m -p $(openssl passwd -1 archer) archie && \
    echo "archie ALL=(ALL) ALL" >> /etc/sudoers

RUN pacman -S python python-pip --noconfirm && \
    pip install "git+https://github.com/DreamingRaven/nemesyst.git#branch=master"
