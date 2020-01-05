FROM archlinux:latest
RUN pacman -Syyuu nvidia python python-pip base-devel git --noconfirm && \
    useradd -m -p $(openssl passwd -1 archer) archie && \
    echo "archie ALL=(ALL) ALL" >> /etc/sudoers
RUN pip install "git+https://github.com/DreamingRaven/nemesyst.git#branch=master"
