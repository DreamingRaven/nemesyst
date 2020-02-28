FROM archlinux:latest

# variable for user username to use in the container
ARG user_name=archie

# variable for user password to use in the container
ARG user_password=archer

# creating basic gpu capable archlinux system
RUN pacman -Syyuu sudo nvidia cuda cudnn git base-devel python python-pip pyalpm fish neovim python-tensorflow-cuda tensorflow-cuda python-future python-configargparse python-pymongo --noconfirm

# creating user with the desired permissions (NOPASS required for pikaur stages)
RUN useradd -m -p $(openssl passwd -1 ${user_password}) ${user_name} && \
    echo "${user_name} ALL=(ALL) ALL" >> /etc/sudoers && \
    echo "${user_name} ALL=(ALL) NOPASSWD:/usr/bin/pacman" >> /etc/sudoers && \
    echo "exec fish" >> /root/.bashrc

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

# install more specific packages from community and AUR as needed, E.G some in-container libs to aid development/ testing:
RUN sudo -u ${user_name} pikaur -S --noconfirm mongodb-bin mongodb-tools-bin python-scikit-learn python-sphinx python-sphinx-argparse python-sphinx_rtd_theme --noconfirm

# changing to final user in case interactivity is desired
USER ${user_name}

RUN echo "cd ~" >> /home/${user_name}/.bashrc && \
    echo "exec fish" >> /home/${user_name}/.bashrc

# RUN echo "${user_password}" | sudo -S pacman -S python-tensorflow-cuda tensorflow-cuda --noconfirm

# get local nemesyst files
COPY --chown=${user_name}:${user_name} . /home/${user_name}/git/nemesyst

# #  OR clone and checkout nemesyst
# RUN cd ~/git && \
#     git clone "https://github.com/DreamingRaven/nemesyst" && \
#     cd ~/git/nemesyst && \
#     git checkout master
