# onliner
Collector for SSH devices. 

If you need to collect output of some show commands from whole network and collect this output to different file.
this is a best tool for it!

Here you can specify the credentials:<br>
PORT=22<br>
USERNAME=""<br>
PASSWORD=""<br>

Folder name<br>
FILEPATH = "/tmp/"   #The directory should be writable!<br>

Here need to specify the devices:<br>
devices = {<br>
    '10.10.10.12':'router01',<br>
    '10.10.10.13':'router02'<br>
    }<br>
<br>
Here need to specify commands that need to be collected:<br>
cmds=["show clock","show chassis","show inventory"]<br>


