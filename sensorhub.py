import json
import math
import bluetooth
from azure.servicebus import ServiceBusService,Message

def readLine(sock):
  msg = ""
  while(len(msg) < 1 or msg[-1:] != "\n"):
    msg += sock.recv(1)
  return msg

def send_buffered(msg, buffer_size, d):
  for i in range(1, int(math.ceil(len(msg) / buffer_size) + 1)):
    startPos = (i - 1) * buffer_size
    stopPos = i * buffer_size
    sendRequest = msg[startPos:stopPos]
    d.send(sendRequest)    
    result = readLine(d)
    if result[:3] != 'ACK':
      print("Error - expected ACK from host, got %s" % result)
      break

#Configure Azure connection
#TODO: put this in a separate config file
key_name = 'RootManageSharedAccessKey' #SharedAccessKeyName
key_value = '' #SharedAccessKey from Azure portal

#Configure Bluetooth connection. Remember to PAIR first!
serverMACAddress = '20:14:05:08:28:64'
port = 1
buffersize = 16
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

#Set up connections
s.connect((serverMACAddress, port))
#sbs = ServiceBusService(service_namespace,
#  shared_access_key_name = key_name,
#  shared_access_key_value = key_value)

Q_HELP = '{"cmd": "%s"}\n' % ("help")
send_buffered(Q_HELP, buffersize, s)
result = readLine(s)

query_format = json.loads(result)

print("Query format = %s" % str(query_format))

#Tear down connections
s.close()
