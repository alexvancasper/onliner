import threading
import paramiko
import socket
from time import sleep
import threading

SSH_PORT=22
TELNET_PORT=23
USERNAME="admin"
PASSWORD="admin"
cmds=["show version"]

def gen_ip_addr(start_ip, end_ip):
    k_start, l_start, m_start, n_start = start_ip.split('.')
    k_end,   l_end,   m_end,   n_end   = end_ip.split('.')
    for k in range(int(k_start), int(k_end)+1):
        for l in range(int(l_start), int(l_end)+1):
            for m in range(int(m_start), int(m_end)+1):
                for n in range(int(n_start), int(n_end)+1):
                  ip_addr = "{}.{}.{}.{}".format(k,l,m,n)
                  yield ip_addr

def write_host(message):
  FILE=open('C:\\output.txt',"a")
  FILE.write(message)
  FILE.close()

def connector(IP):
  global SSH_PORT, USERNAME, PASSWORD
  client = paramiko.SSHClient()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  print ("Connecting to the {} port {}\r".format(IP,SSH_PORT))
  try:
      client.connect(hostname=IP, port=SSH_PORT, username=USERNAME, password=PASSWORD)
  except paramiko.AuthenticationException as e:
     output_ln="Couldn't connect to the host {0} reason: {1}\n".format(IP, e)
     print (output_ln)
     write_host(output_ln)
     return 
  except paramiko.SSHException as e:
     # print ("SSH error host {0} error: {1}".format(IP, e))
     return 
  except socket.error as e:
     # print ("Socket error host {0} error: {1}".format(IP, e))
     return 
  channel = client.invoke_shell()
  channel.set_name('onliner')
  channel.settimeout(0.5)
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
      output_line="Host: {host} Port:{port}".format(host=IP, port=SSH_PORT)
      print(output_line)
      print(buff)
  channel.send("exit\n")
  channel.close()      
def main ():
  threads=[]
  for IP in gen_ip_addr('185.162.233.0','185.162.234.255'):
    t = threading.Thread(target=connector, args=(IP,))
    threads.append(t)
    t.start()


if __name__ == '__main__':
  main()