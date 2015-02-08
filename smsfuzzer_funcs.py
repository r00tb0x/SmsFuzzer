#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Copyright 2014 Paul Kinsella <kali.gsm.rtl.sdr@gmail.com>
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 


import serial, time
import sys
import binascii
import os
import glob
###################################
#	Serial setup
###################################
ser = serial.Serial()
ser.port = "/dev/ttyUSB0" #default so not null
ser.baudrate = 9600
ser.bytesize = serial.EIGHTBITS #number of bits per bytes
ser.parity = serial.PARITY_NONE #set parity check: no parity
ser.stopbits = serial.STOPBITS_ONE #number of stop bits
ser.timeout = 0             #non-block read
ser.xonxoff = False     #disable software flow control
ser.rtscts = False     #disable hardware (RTS/CTS) flow control
ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control



gsm = ("@£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞ\x1bÆæßÉ !\"#¤%&'()*+,-./0123456789:;<=>?"
"¡ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ`¿abcdefghijklmnopqrstuvwxyzäöñüà").decode('utf8')
ext = ("````````````````````^```````````````````{}`````\\````````````[~]`"
"|````````````````````````````````````€``````````````````````````")
#################################
#return serial ports list
#################################
def getOpenSerialPorts():
    	if sys.platform.startswith ('linux'):
    		temp_list = glob.glob ('/dev/tty[A-Za-z]*')
    		result = []
    		for a_port in temp_list:
        		try:
        		    s = serial.Serial(a_port)
        		    s.close()
        		    result.append(a_port)
        		except serial.SerialException:
        		    pass
    	return result

	
def gsm_encode(plaintext):
      res = ""
	    
      for c in plaintext:
	     idx = gsm.find(c);
	     if idx != -1:
		 res += chr(idx)
		 continue
	     idx = ext.find(c)
	     if idx != -1:
		     res += chr(27) + chr(idx)

      return binascii.b2a_hex(res.encode('utf-8'))


########################################################################
#	GET BACK AN AT COMMAND
########################################################################
def getAtReply(serial_port,at_command):
	ser.port = serial_port
        if ser.isOpen() == False:
            ser.open()
	time.sleep(0.3)
        ress =""
	if ser.isOpen():
            ser.flushInput() #flush input buffer, discarding all its contents
            ser.flushOutput()#flush output buffer, aborting current output 
	    sercmd = at_command
            ser.write(sercmd+"\x0D")
            time.sleep(0.2)
            bytesToRead = ser.inWaiting()
            ress = ser.read(bytesToRead)
            ser.close()
	return ress

###############################################################################
#	SWAPS NUMBER EVERY 2 DIGITS USED FOR PDU
#############################################################################
def swapNumber(number):
	swaparray = []
	returnNumber =""
	first1 = 0
	first2 = 1
	second1 =1
	second2 = 2

	for x in range (0,len(number)/2):
		swaparray.append(number[second1:second2])
		swaparray.append(number[first1:first2])
		first1 +=2
		first2 +=2
		second1 +=2
		second2 +=2

	for num in swaparray:
		returnNumber += num
	#print("DEBUG", returnNumber)
	return returnNumber	
	
###############################################################################
#	ENCODE SMS TEXT TO GSM
#############################################################################
def gsm_encode(plaintext):
      res = ""
	    
      for c in plaintext:
	     idx = gsm.find(c);
	     if idx != -1:
		 res += chr(idx)
		 continue
	     idx = ext.find(c)
	     if idx != -1:
		     res += chr(27) + chr(idx)

      return binascii.b2a_hex(res.encode('utf-8'))
###############################################################################
#	ENCODE SMS TEXT TO GSM 8bit
#############################################################################
def gsm_encode8bit(SMS):
	res = ""
	plaintext = SMS
	for c in plaintext:
		idx = gsm.find(c);
		if idx != -1:
			res += chr(idx)
			continue
		idx = ext.find(c)
		if idx != -1:
			res += chr(27) + chr(idx)
	return binascii.b2a_hex(res.encode('utf-8'))
	    #return res.encode('hex')
	    
###############################################################################
#	STRING TO HEX
#############################################################################
def stringToHex(str2hex):
	return str2hex.encode("hex")
###############################################################################
#	STRING TO HEX 18 bit
#############################################################################
def stringToHex18bit(str2hex):
	hexbuffer = ""
	for c in str2hex:
		hexbuffer += '00'+c.encode("hex")
	return hexbuffer	
########################################################################
#			CREATE PDU STRING
# PDU_STRING = createPduString("12345","this is an sms","08",True):
########################################################################

def createPduString(phone_num,sms_text,message_type,del_report_status):
	NUMBER_LEN = len(phone_num)
	NUMBER = phone_num
	SMS_TYPE =message_type

	#If number is odd add an F pdu needs to be even number
	if NUMBER_LEN % 2 != 0:
		NUMBER += "F"
		#print("DEBUG", NUMBER)

	NUMBER = swapNumber(NUMBER)
	NUMBER_LEN_HEX = str(hex(NUMBER_LEN)).lstrip('0x')#GET LEN OF PHONE NUMBER IN HEX

	if NUMBER_LEN <= 15:
		NUMBER_LEN_HEX = "0"+NUMBER_LEN_HEX
	

	smslen = len(sms_text)*2
	MSG_LEN = str(hex(smslen)).lstrip('0x')#get sms data length in hex
	SMS = sms_text
	NUM = phone_num

	if del_report_status == True:
		DEL_REPORT = "21"
	else:
		DEL_REPORT = "01"

	decodedstr1 = stringToHex18bit(sms_text)#gsm_encode(sms_text)

	if smslen <= 15:
		PDU_STRING = "00{0}00{1}91{2}00{3}0{4}{5}".format(DEL_REPORT,NUMBER_LEN_HEX,NUMBER,SMS_TYPE,MSG_LEN,decodedstr1)
	if smslen > 15:
		PDU_STRING = "00{0}00{1}91{2}00{3}{4}{5}".format(DEL_REPORT,NUMBER_LEN_HEX,NUMBER,SMS_TYPE,MSG_LEN,decodedstr1)

	return PDU_STRING

########################################################################
#			CREATE WAP PUSH PDU STRING
# PDU_STRING = createWapPduString(start_date,end_date,header,target_num,msg,wap_type):
########################################################################

def createWapPduString(start_date,end_date,header,target_num,msg,wap_type):
	NUMBER = target_num	
	NUMBER_LEN = len(target_num)#len of num in decimal
	NUMBER_LEN_HEX = str(hex(NUMBER_LEN)).lstrip('0x')#GET LEN OF PHONE NUMBER IN HEX

	if NUMBER_LEN <= 15:
		NUMBER_LEN_HEX = "0"+NUMBER_LEN_HEX
	
	#If number is odd add an F pdu needs to be even number
	if NUMBER_LEN % 2 != 0:
		NUMBER += "F"
		#print("DEBUG", NUMBER)

	NUMBER = swapNumber(NUMBER)


	smslen = len(msg)+ 69
	MSG_LEN_HEX = str(hex(smslen)).lstrip('0x')#get sms data length in hex + the 69 (45 hex)


	WAP_PDU_STRING = "004100{0}91{1}0004{2}0B05040B84C0020003F001010B060403AE81EA02056A0045C6{3}03{4}000AC306{5}10C306{6}0103{7}000101".format(
			NUMBER_LEN_HEX,NUMBER, MSG_LEN_HEX, wap_type, stringToHex(header),start_date,end_date, stringToHex(msg))

	return WAP_PDU_STRING
