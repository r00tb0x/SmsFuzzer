# SmsFuzzer
Send Pdu sms (SILENT FLASH or NORMAL)

Simple little app to test your modem or phone to see if it can send SILENT SMS etc.

Number has to be in international format.
(important)
Press pdu mode button to put modem in pdu mode if you dont do this the app wont send your sms.

Code works on my phone and modem and havent tested any other modems, if it works on yours please email the model and make so I can make a list for other people.


First try a normal sms to see if it sends and then a flash, if your target phone gets them your modem can send SILENT sms.

If one port doesnt work try another etc.

Coded this on kali linux but should work fine on ubuntu.
Make sure you have wxPython installed.

You might have to chmod 775 ./smsfuzzer.py and the other file if they dont run.

To start go to the folder where files are and type ./smsfuzzer.py

Enjoy:)

#WAP PUSH SMS

Use the wap_push-py.py file to send wap push sms.

#HOW TO USE

1. Select serial port
2. Type in start date and end date in the format in the text box. (Important if the end date isnt greater than the current date the user will not get the sms, its another form of silent sms if the date < current date).
3. Enter header example www.yourheader.com (Important: header length has to be 18 digits len and no greater, if your header isnt 18 digits in length use spaces to make it 18.
4. Enter target number in international format without + sign
5. Enter sms to be sent (Important: sms can not be greater than 70 characters)
6. make sure modem/phone is in pdu mode
7. Press send button.

You probably have to chmod 775 wap_push_py.py to get this file to run.

Users phone has to have allow wap push messages active from them to get the message.

What it looks like on a phone

https://www.dropbox.com/s/uhrebenxgh3hbj9/wap1.png?dl=0

https://www.dropbox.com/s/l8kh8u5w86roa94/wap2.png?dl=0
