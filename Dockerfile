FROM conda/miniconda3

WORKDIR /downloads

RUN apt-get update -y \
    && apt-get install -y \
    uuid \
    uuid-dev \
    build-essential \
#    libcppunit \
    libcppunit-dev \
    libapr1 \
    libapr1-dev \
    wget \
    autoconf \
    automake \
    libtool \
    git \

RUN git clone https://gitbox.apache.org/repos/asf/activemq-cpp.git \
    && cd activemq-cpp/activemq-cpp \
    && ./autogen.sh \
    && ./configure \
    && make \
    && make install

RUN git clone https://github.com/joedurbak/tcs_client.git \
    && cd tcs_client/lowell_proc05 \
#    && make \
#    && make install

RUN alias ls='ls --color=auto'
