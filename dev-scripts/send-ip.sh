#!/bin/bash

i=$(ip addr | grep 'state UP' -A2 | tail -n1 | awk '{print $2}' | cut -f1  -d'/')
h=$(hostname)
curl --request GET "https://www.doc.ic.ac.uk/~ah4515/moderntimes/ip_save.php?hostname=$h&ip=$i"
