FROM python


WORKDIR /usr/src
COPY ta-lib-0.4.0-src.tar.gz /usr/src/
RUN tar -xzf ta-lib-0.4.0-src.tar.gz
WORKDIR /usr/src/ta-lib
RUN ./configure --prefix=/usr
RUN make
RUN make install

WORKDIR /usr/src
RUN pip install requests
RUN pip install bs4
RUN pip install pandas
RUN pip install TA-Lib
RUN pip install colorama



