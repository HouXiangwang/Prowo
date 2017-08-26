FROM opengn.org:32333/easypi/alpine-arm
MAINTAINER joliu<joliu@s-an.org>
WORKDIR /data
RUN apk --update add python3 py3-pip tzdata
RUN pip3 install pymysql
ENV TIME_ZONE Asia/Shanghai
COPY tcpclient.py /data
COPY tcpserver.py /data
RUN echo "${TIME_ZONE}" > /etc/timezone \
&& ln -sf /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime 

CMD python3 /data/tcpserver.py
