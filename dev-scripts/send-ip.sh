#!/bin/bash

i=$(ifconfig | awk -F':' '/inet addr/&&!/127.0.0.1/{split($2,_," ");print _[1]}')
h=$(hostname)
curl --request GET "https://www.doc.ic.ac.uk/~ah4515/moderntimes/ip_save.php?hostname=$h&ip=$i"
