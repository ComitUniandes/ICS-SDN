"""
PLC 1
"""

from minicps.devices import PLC
from utils import *

import time
from threading import Thread

import socket
import json
import select

MV101 = ('MV101', 1)
LIT101 = ('LIT101', 1)
P101 = ('P101', 1)

LIT301 = ('LIT301', 3)

SENSOR_ADDR = IP['lit101']
IDS_ADDR = IP['ids101']
PLC301_ADDR = IP['plc301']

# TODO: real value tag where to read/write flow sensor

class Lit301Socket(Thread):
    """ Class that receives water level from the water_tank.py  """

    def __init__(self, plc_object):        
        Thread.__init__(self)
        self.plc = plc_object

    def run(self):
        print "DEBUG entering socket thread run"
        self.sock = socket.socket()     # Create a socket object    
        self.sock.bind((IP['plc101'] , 8754 ))
        self.sock.listen(5)

        while (self.plc.count <= PLC_SAMPLES):
            try:
            	client, addr = self.sock.accept()
		data = client.recv(4096)                                                # Get data from the client         
            
            	message_dict = eval(json.loads(data))
	        lit301 = float(message_dict['Variable'])

	        print "received from LIT301!", lit301

            
	        if lit301 >= LIT_301_M['HH'] :
                    #self.plc.send(P101, 0, IP['plc101'])                  
	            self.send_message(IP['p101'], 7842 , 0)

	        elif lit301 >= LIT_301_M['H']:
                    #self.plc.send(P101, 0, IP['plc101'])
	            self.send_message(IP['p101'], 7842 , 0)

                elif lit301 <= LIT_301_M['LL']:
                    #self.plc.send(P101, 1, IP['plc101'])
                    self.send_message(IP['p101'], 7842 , 1)

            	elif lit301 <= LIT_301_M['L']:
                    #self.plc.send(P101, 1, IP['plc101'])
                    self.send_message(IP['p101'], 7842 , 1)


            except KeyboardInterrupt:
 	        print "\nCtrl+C was hitten, stopping server"
                client.close()
        	break


    def send_message(self, ipaddr, port, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ipaddr, port))

        msg_dict = dict.fromkeys(['Type', 'Variable'])
        msg_dict['Type'] = "Report"
        msg_dict['Variable'] = message
        message = json.dumps(str(msg_dict))

        try:
            ready_to_read, ready_to_write, in_error = select.select([sock, ], [sock, ], [], 5)
        except:
            print "Socket error"
            return
        if(ready_to_write > 0):
            sock.send(message)
        sock.close()


class IdsSocket(Thread):
    """ Class that receives water level from the water_tank.py  """

    def __init__(self, plc_object):        
        Thread.__init__(self)
        self.plc = plc_object

    def run(self):
        print "DEBUG entering socket thread run"
        self.sock = socket.socket()     # Create a socket object    
        self.sock.bind((IP['plc101'] , 4234 ))
        self.sock.listen(5)

        while (self.plc.count <= PLC_SAMPLES):
            try:
	        client, addr = self.sock.accept()
		data = client.recv(4096)                                                # Get data from the client         

		#lit101 = float(self.plc.recieve(LIT101, IDS_ADDR))
	        message_dict = eval(json.loads(data))
	        lit101 = float(message_dict['Variable'])
		print "received from IDS!", lit101

            
	        #print 'DEBUG plc1 lit101: %.5f' % lit101

	        if lit101 >= LIT_101_M['HH'] :
	            #self.plc.send(MV101, 0, IP['plc101'])
               	    mv = 0

	        elif lit101 >= LIT_101_M['H']:
	            #self.plc.send(MV101, 0, IP['plc101'])
                    mv = 0

	        elif lit101 <= LIT_101_M['L']:
	            #self.plc.send(MV101, 1, IP['plc101'])
                    mv = 1

	        elif lit101 <= LIT_101_M['LL']:
	            #self.plc.send(MV101, 1, IP['plc101'])                
                    mv = 1

                self.send_message(IP['mv101'], 9587, mv)
       	    except KeyboardInterrupt:
	    	print "\nCtrl+C was hitten, stopping server"
	        client.close()
		break

    def send_message(self, ipaddr, port, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ipaddr, port))

        msg_dict = dict.fromkeys(['Type', 'Variable'])
        msg_dict['Type'] = "Report"
        msg_dict['Variable'] = message
        message = json.dumps(str(msg_dict))

        try:
            ready_to_read, ready_to_write, in_error = select.select([sock, ], [sock, ], [], 5)
        except:
            print "Socket error"
            return
        if(ready_to_write > 0):
            sock.send(message)
        sock.close()        

class PLC101(PLC):

    def pre_loop(self, sleep=0.1):
        print 'DEBUG: swat-s1 plc1 enters pre_loop'
        time.sleep(sleep)

    def main_loop(self):
        """plc1 main loop.

            - reads sensors value
            - drives actuators according to the control strategy
            - updates its enip server
        """

        print 'DEBUG: swat-s1 plc1 enters main_loop.'

        lit301socket = Lit301Socket(self)
        lit301socket.start()
        self.count = 0
        backup = IdsSocket(self)
	backup.start()
        while(self.count <= PLC_SAMPLES):

            # lit101 [meters]
	    try:
	    	lit101 = float(self.receive(LIT101, SENSOR_ADDR))
	        #print 'DEBUG plc1 lit101: %.5f' % lit101
		print "plc1 lit101", lit101

	        if lit101 >= LIT_101_M['HH'] :
                   self.send(MV101, 0, IP['plc101'])

                elif lit101 >= LIT_101_M['H']:
                   self.send(MV101, 0, IP['plc101'])

                elif lit101 <= LIT_101_M['L']:
                   self.send(MV101, 1, IP['plc101'])

                elif lit101 <= LIT_101_M['LL']:
                   self.send(MV101, 1, IP['plc101'])

	    except:
		   print "Switching to backup"
		   break


if __name__ == "__main__":

    plc101 = PLC101(name='plc101',state=STATE,protocol=PLC101_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)
    #plc1.pre_loop()
    #plc1.main_loop()
