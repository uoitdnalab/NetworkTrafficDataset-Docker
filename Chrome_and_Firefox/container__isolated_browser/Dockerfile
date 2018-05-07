FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y vnc4server jwm firefox
RUN apt-get install -y tcpdump

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y tshark

RUN apt-get install -y nano
RUN apt-get install -y python
RUN apt-get install -y python-scapy
RUN apt-get install -y mitmproxy
RUN apt-get install -y xautomation
RUN apt-get install -y python-flask
RUN apt-get install -y python-jinja2
RUN apt-get install -y python-networkx
RUN apt-get install -y python-pexpect


# Update the image
RUN echo "random904859" # Change to break cache and cause update/upgrade
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get -y install firefox
RUN apt-get -y install chromium-browser

RUN apt-get -y install scrot
RUN apt-get -y install netcat-openbsd

ADD startup_script.sh /startup_script.sh
RUN chmod +x /startup_script.sh

ADD mypass /mypass
ADD bookmarklet.js /bookmarklet.js
ADD make_basegraph.py /make_basegraph.py
ADD add_to_graph.py /add_to_graph.py
ADD extend_graph.py /extend_graph.py
ADD resolve_leaves.py /resolve_leaves.py
ADD ChromeHandler.py /ChromeHandler.py
ADD DOMUtilities.py /DOMUtilities.py
ADD oneliner.js /oneliner.js
ADD oneline_label_top_n.min.js /oneline_label_top_n.min.js
ADD PageStateUtils.py /PageStateUtils.py
ADD popup_server.py /popup_server.py

ADD generate_js_commands.py /generate_js_commands.py
ADD command_server.py /command_server.py
ADD dom_set_server.py /dom_set_server.py


ADD capture_command.sh /capture_command.sh
RUN chmod +x /capture_command.sh

ADD crawl_in_firefox.sh /crawl_in_firefox.sh
RUN chmod +x /crawl_in_firefox.sh

ADD make_reddit_network.sh /make_reddit_network.sh
RUN chmod +x /make_reddit_network.sh

ADD popup_server_test.py /popup_server_test.py

RUN mkdir /__doms
RUN mkdir /__samples
RUN mkdir /__generated_commands
RUN mkdir /__screenshots

RUN echo "1532"
RUN apt-get update
RUN apt-get -y upgrade

#Set environment variables
ENV DISPLAY :0

CMD ./startup_script.sh
