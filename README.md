READ ME 
If u have this , you wanna know how it works 
has 2 modes, kinda, can works both at the same time


BLUETOOTH TUTORIAL 
First on the server machine launch server.py (inside Server Folder)
Then launch BluetoothServer.py (Also in the Server Folder) 
make sure pairable AND discoverable is ON
from the the client pair the computurs 
then Launch Bluetooth.py (client side , Client Folder)
THEN launch Bluetoothclient.py (client side too, Client Folder)
## Make sure to to change the MAC addresses in the BluetoothServer.py and BluetoothClient.py to YOUR server's MAC address

NORMAL / LAN CONNECTIONS
run server.py (Location above)
run local.py (Client folder)
Input server.py's IP in local.py




GENERAL / BOTH OF THEM
Usernames 1 time per sessions (if u log out you cant use the same username till u restart the server, might fix that next time)
Encryption keys aren't generated , you manually input an agreed key , otherwise the chat WILL be encrypted it will not be readable (Even capitalaisation matters)


(This was a fun lil project a made in school to bypass some annoying network policies , so thats the deal with the bluetooth)
