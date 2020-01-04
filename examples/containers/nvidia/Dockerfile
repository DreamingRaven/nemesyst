FROM archlinux:latest
RUN pacman -Syyuu --noconfirm && \
    useradd -m -p $(openssl passwd -1 archer) archie 
RUN pacman -S nvidia python base-devel --noconfirm
