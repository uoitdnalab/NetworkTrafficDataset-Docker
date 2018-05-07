FROM jupyter/datascience-notebook
USER root
COPY scapy-2.4.0.tar.gz /
ADD install_scapy.sh /
RUN chmod +x /install_scapy.sh
RUN /install_scapy.sh
USER jovyan
RUN pip install ruptures
