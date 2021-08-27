FROM ubuntu
RUN apt update && apt install -y git make autoconf libtool libssl-dev
RUN git clone https://github.com/Netflix/dynomite.git && cd dynomite && autoreconf -fvi && CFLAGS="-ggdb3 -O0" ./configure --enable-debug=full && make && make install
ENTRYPOINT [ "dynomite"]

