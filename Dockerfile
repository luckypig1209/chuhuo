FROM python:latest as auto_db

ADD jenkins/autodb.py /opt/autodb.py
ADD E10CN /opt/E10CN
ADD E10TW /opt/E10TW

ARG MODULE
ARG tenantId
ARG tenantSid
RUN echo "MODULE: ${MODULE}"
RUN echo "tenantId: ${tenantId}"
RUN echo "tenantSid: ${tenantSid}"
#RUN pip3 install pymysql impyla
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pymysql impyla

WORKDIR /opt
#RUN apt update && apt -y install telnet
#RUN python3 autodb.py ${MODULE} ${tenantId} ${tenantSid}

CMD     ["/bin/bash"]
