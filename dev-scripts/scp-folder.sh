#!/bin/bash

# variable a is the path to the azure-mt.file
a="~/modern-times/dev-scripts/azure-mt.rsa"

# First argument ($1) is the local path to the source file
# Second argument ($2) is the server path to the destination after ~/
scp -i $a -r $1 moderntimes@modern-times-1.uksouth.cloudapp.azure.com:~/

