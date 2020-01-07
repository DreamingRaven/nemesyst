FROM archlinux:latest

# variable for user username to use in the container
ARG user_name=archie

# variable for user password to use in the container
ARG user_password=archer

# variable for which branch to use of nemesyst when installing it
ARG branch=master

# creating basic gpu capable archlinux system with user and python
RUN pacman -Syyuu sudo nvidia git base-devel python python-pip pyalpm --noconfirm && \
    useradd -m -p $(openssl passwd -1 ${user_password}) ${user_name} && \
    echo "${user_name} ALL=(ALL) ALL" >> /etc/sudoers

# swapping to our newly created user
USER ${user_name}

# clone, build, and install pikaur
RUN mkdir ~/git && \
    cd ~/git && \
    git clone "https://aur.archlinux.org/pikaur.git" && \
    cd ~/git/pikaur && \
    echo "${user_password}" | makepkg -s --noconfirm && \
    echo "${user_password}" | sudo -S pacman -U pikaur*pkg.tar.xz --noconfirm

# building cuda enabled tensorflow
RUN pikaur -S tensorflow-cuda-git --noconfirm

# clone, swap to desired branch, of nemesyst
RUN cd ~/git && \
    git clone "https://github.com/DreamingRaven/nemesyst" && \
    cd ~/git/nemesyst && \
    git checkout ${branch}
