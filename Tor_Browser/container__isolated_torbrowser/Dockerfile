FROM ubuntu:latest

RUN apt-get update
RUN apt-get -y upgrade

RUN apt-get install -y vnc4server jwm
RUN apt-get install -y nano
RUN apt-get install -y libasound2
RUN apt-get install -y xz-utils
RUN apt-get install -y tcpdump
RUN apt-get install -y python python-flask
RUN apt-get install -y xautomation
RUN apt-get install -y wmctrl
RUN apt-get install -y scrot
RUN apt-get install -y netcat-openbsd

RUN apt-get install -y software-properties-common

RUN add-apt-repository ppa:micahflee/ppa
RUN apt-get update
RUN apt-get install -y torbrowser-launcher

ADD mypass /mypass

ADD startup_script.sh /startup_script.sh

RUN chmod +x /startup_script.sh

#Set environment variables
ENV DISPLAY :0

RUN useradd -m -d /home/anon anon
WORKDIR /home/anon

ADD mypass /home/anon/mypass
RUN chmod +r /home/anon/mypass

ADD bookmarklet.js /home/anon/bookmarklet.js

ADD command_server.py /command_server.py
ADD dom_set_server.py /dom_set_server.py

RUN mkdir /__screenshots
RUN chown anon /__screenshots
RUN chmod 777 /__screenshots

#RUN groupadd pcap
#RUN usermod -a -G pcap anon
#RUN chgrp pcap /usr/sbin/tcpdump
#RUN chmod 750 /usr/sbin/tcpdump
#RUN setcap cap_net_raw,cap_net_admin=eip /usr/sbin/tcpdump

ADD capture_command.sh /capture_command.sh
RUN chmod +x /capture_command.sh

ADD generate_ssl_cert.sh /generate_ssl_cert.sh
RUN chmod +x /generate_ssl_cert.sh
RUN /generate_ssl_cert.sh

RUN mkdir /home/anon/Downloads && \
	chown anon:anon /home/$USER && \
	chown anon:anon /home/$USER/* && \
	apt-get autoremove

#USER anon

CMD /startup_script.sh

