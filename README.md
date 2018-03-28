# azure-dq-purger
Purges Dead Queue Messages From Azure Service Bus Queue. 

## Commands
Had Anaconda3 installed and set as my default Python executable.

### Install Commands
```text
pip install azure-servicebus
```

### Script Commands
```text
python purger.py --namespace foobar.servicebus.windows.net --buskeyname RootManageSharedAccessKey --buskeyvalue foobar --queue foo --get 50
```
