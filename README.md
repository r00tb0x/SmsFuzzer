# SmsFuzzer
Send Pdu sms (SILENT FLASH or NORMAL)

Simple little app to test your modem or phone to see if it can send SILENT SMS etc.

Number has to be in international format.

Code works on my phone and modem and havent tested any other modems, if it works on yours please email the model and make so I can make a list of other people.


First try a normal sms to see if it sends and then a flash, if your target phone gets them your modem can send SILENT sms.

If one port doesnt work try another etc.

Coded this kali linux but should work fine on ubuntu.
Make sure you have wxPython installed.

You might have to chmod 775 ./smsfuzzer.py and the other file if they dont run.

To start simple go to the folder with files are and type ./smsfuzzer.py

Enjoy:)
