import threading
import paramiko
import socket
from time import sleep

# How to start the script
# $ python3.5 onliner.py 
# while the script is collectin necessary data need to wait
# $
# $ cd /tmp (FILEPATH) and you sould see necessary files
# That's all

PORT=22
USERNAME=""
PASSWORD=""
FILEPATH = "/tmp/"   #The directory should be writable!

devices = {
    '10.10.10.12':'router01',
    '10.10.10.13':'router02'
    }

cmds=[
"show commands",
"show commands",
"show commands" ]


def write_to_file(in_lines, nodename):
  global FILEPATH
  if len(in_lines)>0:
    FILE=open(FILEPATH+nodename+".log","a")
    for line in in_lines:
      FILE.write(line+"\n")
    FILE.close()

def parser(buff, cmd, nodename):
    new_buff = buff.decode("utf-8")
    in_lines=new_buff.split("\r\n")
    if "show" in cmd:
      write_to_file(in_lines, nodename)
      
def main ():
    for HOST in devices:
      # print(devices[HOST])
      client = paramiko.SSHClient()
      client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      try:
          client.connect(hostname=HOST, port=PORT, username=USERNAME, password=PASSWORD)
      except paramiko.AuthenticationException as e:
         print ("Couldn't connect: to the host {0} reason: {1}".format(HOST, e))
         break
      except paramiko.SSHException as e:
         print ("SSH error host {0} error: {1}".format(HOST, e))
         break
      except socket.error as e:
         print ("Socket error host {0} error: {1}".format(HOST, e))
         break
      channel = client.invoke_shell()
      channel.set_name('onliner')
      channel.settimeout(1)
      channel.send("terminal length 0"+"\n")
      for cmd in cmds:
        buff=b''
        channel.send(cmd+"\n")
        sleep(0.5)
        if channel.recv_ready():
          while not (buff.endswith(b"# ") or buff.endswith(b'>')):
             try:
                buff+=channel.recv(128)
             except socket.timeout as e:
                break
        if len(buff)>0:
           parser_thread = threading.Thread(target=parser, args=(buff,cmd,devices[HOST],))
           parser_thread.start()
           parser_thread.join()
      channel.send("exit\n")
      channel.close()

if __name__ == '__main__':
  main()