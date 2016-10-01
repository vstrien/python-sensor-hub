# python-sensor-hub
Azure IoT Sensor Hub implementing the KSN protocol.

Provides an easy PoC demonstrating how to communicate sensor values towards
Azure.

The DeviceClient-class I use is written by @bechynsky and forked from 
https://github.com/bechynsky/AzureIoTDeviceClientPY.

Notice the SensorToCloud module uses pybluez.

Sample code:
```python
import DeviceClient
import SensorToCloud

#Set up Azure connection
KEY = "Device key from Azure IoT" 
HUB = "Name of your Azure IoT Hub"
DEVICE_NAME = "Device Name from Azure IoT"

azure_client = DeviceClient.DeviceClient(HUB, DEVICE_NAME, KEY)


#Configure Bluetooth connection. Remember to PAIR first!
BT_MAC_addr = "MAC address of your KSN-style sensor"
port = 1
buffersize = 16
        
#Set query constants for your particular sensor.
Q_TEMP_CURRENT = "{\"cmd\": \"query\", \"params\": {\"SensorType\": \"TempC\", \"ValueType\": \"current\"}}\n";
Q_HUMIDITY_CURRENT = "{\"cmd\": \"query\", \"params\": {\"SensorType\": \"Humidity\", \"ValueType\": \"current\"}}\n";

stc = SensorToCloud.SensorToCloud(azure_client, BT_MAC_addr, port, 
  buffersize, [Q_TEMP_CURRENT, Q_HUMIDITY_CURRENT])


while(True):
  stc.queryAllToCloud()
  time.sleep(5)
```
