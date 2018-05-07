#!/bin/bash

#Create the JSON graph file
python make_basegraph.py reddit_network.yml

#Add the first order nodes
setterm --foreground cyan
echo 'First order nodes'
python add_to_graph.py reddit_network.yml https://www.reddit.com in_docker

#Resolve the leaves
setterm --foreground magenta
python resolve_leaves.py reddit_network.yml https://www.reddit.com with_browser in_docker

#Get the second order nodes
echo 'Second order nodes'
setterm --foreground green
python extend_graph.py reddit_network.yml https://www.reddit.com with_browser in_docker

#Resolve the leaves
setterm --foreground red
python resolve_leaves.py reddit_network.yml https://www.reddit.com with_browser in_docker

#Get the third order nodes
setterm --foreground yellow
echo 'Third order nodes'
python extend_graph.py reddit_network.yml https://www.reddit.com with_browser in_docker

#Resolve the leaves
setterm --foreground blue
python resolve_leaves.py reddit_network.yml https://www.reddit.com with_browser in_docker

#Create a directory for the navigation commands
mkdir /reddit_network_navigation_commands

setterm --foreground white
#Generate commands for all browsers
python generate_js_commands.py reddit_network.yml https://www.reddit.com /reddit_network_navigation_commands
