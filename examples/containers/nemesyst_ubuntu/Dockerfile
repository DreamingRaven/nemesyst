FROM ubuntu:19.04

# updating and installing basic ubuntu python container
RUN apt update && \
    apt install -y wget python3.7 python3-pip git

# getting and installing tensorflow, and tf-seal
RUN wget https://storage.googleapis.com/tf-pips/tf-c++17-support/tf_nightly-1.14.0-cp37-cp37m-linux_x86_64.whl && \
    python3.7 -m pip install tf_nightly-1.14.0-cp37-cp37m-linux_x86_64.whl && \
    rm tf_nightly-1.14.0-cp37-cp37m-linux_x86_64.whl && \
    python3.7 -m pip install tf-seal

# getting tf-seal repository so we have access to all of their examples etc
RUN python3.7 -m pip install git+https://github.com/DreamingRaven/nemesyst.git#branch=master && \
    git clone https://github.com/tf-encrypted/tf-seal && \
    git clone https://github.com/DreamingRaven/nemesyst
