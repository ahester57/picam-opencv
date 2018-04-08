### picam-opencv
#### Austin Hester

This script is to be run like:  

```nc -l <port> | python -u cvtest.py```

On the Raspberry Pi with camera enabled, run the command:  

```raspivid -t 0 -w 960 -h 800 -o - | nc <server-ip> <port>```

after starting the script on your PC.


