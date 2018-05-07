FROM ubuntu:latest

RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get -y install nano
RUN apt-get -y install python
RUN apt-get -y install python-flask
RUN apt-get -y install python-imaging
RUN apt-get -y install openssl
RUN apt-get -y install netcat-openbsd

ADD capture_command.sh /capture_command.sh
RUN chmod +x /capture_command.sh

ADD bookmarklet.js /bookmarklet.js
ADD tcpdump_polyfill.py /tcpdump_polyfill.py
ADD advance_signal.py /advance_signal.py
ADD dom_set_server.py /dom_set_server.py
ADD command_server.py /command_server.py
ADD msedge_click_bookmarklet.py /msedge_click_bookmarklet.py
ADD msedge_close_window.py /msedge_close_window.py
ADD msedge_navigate_aboutblank.py /msedge_navigate_aboutblank.py
ADD msedge_open_private.py /msedge_open_private.py
ADD msedge_take_screenshot.py /msedge_take_screenshot.py
ADD QEMU_MouseKey.py /QEMU_MouseKey.py

ADD empty_qemu_pipe.sh /empty_qemu_pipe.sh
RUN chmod +x /empty_qemu_pipe.sh

ADD generate_ssl_cert.sh /generate_ssl_cert.sh
RUN chmod +x /generate_ssl_cert.sh
RUN /generate_ssl_cert.sh

ENTRYPOINT ["bash"]
