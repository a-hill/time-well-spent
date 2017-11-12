#!/bin/bash

# Need to install az CLI, and then run the login script (az login), first
az vm deallocate --resource-group modern-times-rg --name modern-times-1
