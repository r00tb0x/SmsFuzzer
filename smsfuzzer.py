#!/usr/bin/env python

# Copyright 2015 Paul Kinsella <kali.gsm.rtl.sdr@gmail.com>
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

import wx
from smsfuzzer_funcs import * 

mySerialPort = serial.Serial()
mySerialPort.port = 	"/dev/ttyUSB0" #default so not null
mySerialPort.baudrate = 9600
mySerialPort.bytesize = serial.EIGHTBITS #number of bits per bytes
mySerialPort.parity = 	serial.PARITY_NONE #set parity check: no parity
mySerialPort.stopbits = serial.STOPBITS_ONE #number of stop bits
mySerialPort.timeout = 	0             #non-block read
mySerialPort.xonxoff = 	False     #disable software flow control
mySerialPort.rtscts = 	False     #disable hardware (RTS/CTS) flow control
mySerialPort.dsrdtr = 	False       #disable hardware (DSR/DTR) flow control


FLASH1 = 	"10"#4 bit encoding
FLASH2 = 	"14"#8 bit encoding
FLASH3 = 	"18"
SILENT = 	"C0"
NORMAL = 	"04"


class ExampleFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self,parent,size=(220,200),title='Sms Fuzzer')
        panel = wx.Panel(self)

	#####################################################
	#MISC FUCTIONS
	#####################################################
	tested_ports = getOpenSerialPorts()
	if len(tested_ports) < 1:
		tested_ports.append("NO PORTS")

	#####################################################
	#BUTTON FUCTIONS
	#####################################################
	def onPduModeClick(event):
        	wx.MessageBox(getAtReply(self.combo_serial_ports.GetValue(),"AT+CMGF=0"), 'Info', 
            	wx.OK | wx.ICON_INFORMATION)
		
	def on2gModeClick(event):
        	wx.MessageBox(getAtReply(self.combo_serial_ports.GetValue(),"AT^SYSCFG=13,1,3FFFFFFF,2,4"), 'Info', 
            	wx.OK | wx.ICON_INFORMATION)


	def onSendClick(event):
		mySerialPort.port = self.combo_serial_ports.GetValue()
		DEL_REPORT_STATUS = self.cb_report.GetValue()

		smstype = self.combo_sms_type.GetValue()
		if smstype == "SILENT":
			SMS_TYPE = SILENT
		if smstype == "NORMAL":
			SMS_TYPE = NORMAL
		if smstype == "FLASH":
			SMS_TYPE = FLASH2

		if mySerialPort.open() == False:
			mySerialPort.open()
	
		if mySerialPort.isOpen():
			mySerialPort.flushInput() #flush input buffer, discarding all its contents
        		mySerialPort.flushOutput()#flush output buffer, aborting current output
			mySerialPort.write("AT+CMGS=17"+"\x0D")
                        PDU_STRING = createPduString(self.edit_target_number.GetValue(),self.edit_target_msg .GetValue(),SMS_TYPE,DEL_REPORT_STATUS)
			time.sleep(0.3)
			mySerialPort.write(PDU_STRING+"\x1A")
			time.sleep(0.3)
			bytesToRead = mySerialPort.inWaiting()
			ress = mySerialPort.read(bytesToRead)
        		wx.MessageBox(ress, 'Info', 
            		wx.OK | wx.ICON_INFORMATION)
		else:
			wx.MessageBox('Message did not send', 'Info', 
            		wx.OK | wx.ICON_INFORMATION)

		mySerialPort.close()

	self.lb_comport = wx.StaticText(panel, label="Com Port:",pos=(5,5))
	self.combo_serial_ports = wx.ComboBox(panel,size=(135,30), pos=(80,5), choices=tested_ports, style=wx.CB_READONLY)
	self.combo_serial_ports.SetSelection(0)

	self.lb_smstype = wx.StaticText(panel, label="Sms Type:",pos=(5,35))
	self.combo_sms_type = wx.ComboBox(panel,size=(135,30), pos=(80,35), choices=['NORMAL','FLASH','SILENT'], style=wx.CB_READONLY)
	self.combo_sms_type.SetSelection(0)

	self.lb_target = wx.StaticText(panel, label="Target No:",pos=(5,65))
	self.edit_target_number = wx.TextCtrl(panel,size=(135,30), pos=(80,65),value='123456789012')

	self.lb_target_data = wx.StaticText(panel, label="Sms Msg:",pos=(5,95))
	self.edit_target_msg = wx.TextCtrl(panel,size=(135,60), pos=(80,95),value='Hello World',style=wx.TE_MULTILINE)

	self.cb_report = wx.CheckBox(panel,-1,'Del\nReport', pos=(5,110),size=(80,50))
	self.cb_report.SetValue(True)

	self.btnpdumode = wx.Button(panel, label="Pdu Mode",pos=(5,155),size=(85,25))
	self.btnpdumode.Bind(wx.EVT_BUTTON,onPduModeClick)

	self.btn2g_mode = wx.Button(panel, label="2G Mode",pos=(90,155),size=(80,25))
	self.btn2g_mode.Bind(wx.EVT_BUTTON,on2gModeClick)

	self.btnsend = wx.Button(panel, label="Send",pos=(170,155),size=(45,25))
	self.btnsend.Bind(wx.EVT_BUTTON,onSendClick)

	self.lb_output = wx.StaticText(panel, label="Debug:",pos=(5,180))


	



app = wx.App(False)
frame = ExampleFrame(None)
frame.Show()
app.MainLoop()
