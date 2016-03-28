import time
import json
import math
import bluetooth

class SensorToCloud():
  """
    Client to connect a sensor using KSN v0.1 to the Azure Cloud
    using the DeviceClient-class
  """

  """
    Reads a line from a socket. Returns as soon as a newline is encountered.
  """
  def read_line(self, sock):
    msg = ""
    while(len(msg) < 1 or msg[-1:] != "\n"):
      msg += sock.recv(1).decode("utf-8")
    return msg
  
  """
    Sends a message in chunks of *buffer_size*.
    After *buffer_size* bytes are sent, waits for 'ACK' from device.
  """
  def send_buffered(self, msg, d):
    bf = self.buffersize
    for i in range(1, int(math.ceil(len(msg) / (bf * 1.0)) + 1)):
      startPos = (i - 1) * bf
      stopPos = i * bf
      sendRequest = msg[startPos:stopPos]
      d.send(sendRequest)    
      result = self.read_line(d)
      if result[:3] != 'ACK':
        raise Exception("Error - expected ACK from host, got %s" % result)
  
  """
    Send queries to device, results to cloud
  """
  def queryAllToCloud(self):
    s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    s.connect((self.device_address, self.port))
    "Create SAS (security token) valid for 60 seconds"
    self.azure_client.create_sas(60)
    
    for query in self.queries:
      self.send_buffered(query, s)
      query_result = self.read_line(s)
      self.azure_client.send(query_result.encode("utf-8"))
    
    s.close
   
  def __init__(self, device_client, bt_mac_addr, port, bufsize, queries):
    self.azure_client = device_client
    self.device_address = bt_mac_addr
    self.port = port
    self.buffersize = bufsize
    self.queries = queries
