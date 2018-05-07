# Jupyter Notebooks

Builds a Docker container capable of running the network traffic
analysis examples found in our dataset paper.

Building
--------

Build with the command:
```
docker build -t network-traffic-notebook .
```

Running
-------

Run with the command:
```
docker run -it -p 127.0.0.1:8888:8888 network-traffic-notebook
```

Example - Measuring Page Load Time
----------------------------------

- Upload the network capture file
`TrafficSamples/TorBrowser/8e63dc9826b53c29c3a123762f4b7091cd6dfea06dd8897f7b3d7e3681524c41.pcap`
through the Jupyter Web Interface.
- Load the Jupyter Notebook `Load Time Measurement.ipynb`.


Example - Web Page Identification via Traffic Pattern Analysis
---------------------------------------------------------------

- In Jupyter create the directories `PageIdentificationSamples/MsEdge`,
`PageIdentificationSamples/TorBrowser`,
`PageIdentificationSamples/Firefox`
- Upload all network capture files into their appropriate directories
through the Jupyter Web Interface.
- Load the Jupyter Notebook `Webpage Identification.ipynb`.
