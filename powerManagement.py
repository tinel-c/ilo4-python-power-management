from password import *
import paramiko
import re
import paho.mqtt.client as mqtt

def hpServerStatus():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(iloIpAddress, username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command('POWER')
    ouput = str(stdout.read())
    #print (ouput)
    powerStatus = re.search('server(.*)\\\\r\\\\n\\\\r\\\\n', ouput)
    stringPowerStatus = powerStatus.group(1)
    print('Server'+stringPowerStatus)

def hpServerOn():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(iloIpAddress, username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command('POWER on')
    ouput = str(stdout.read())
    #print (ouput)
    powerStatus = re.search('Server(.*)\\.', ouput)
    stringPowerStatus = powerStatus.group(1)
    print('Server'+stringPowerStatus)

def hpServerOff():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(iloIpAddress, username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command('POWER off')
    ouput = str(stdout.read())
    #print (ouput)
    powerStatus = re.search('Server(.*)\\.', ouput)
    stringPowerStatus = powerStatus.group(1)
    print('Server'+stringPowerStatus)

hpServerOn()