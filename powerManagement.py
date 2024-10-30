from password import *
import paramiko
import re
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import time, threading

publishStatusTopic = "hpServerStatus/state"
publishStatusTimeTopic = "hpServerStatus/timestamp"
powerManagementStatusTopic = "hpServerStatus/powerManagementStatus"
powerManagementRequestTopic = "hpServerStatus/powerManagement"

mqttHostName = "192.168.2.4"

def hpServerStatus():
    ssh = None
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(iloIpAddress, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command('POWER')
        ouput = str(stdout.read())
        #print (ouput)
        powerStatus = re.search('server(.*)\\\\r\\\\n\\\\r\\\\n', ouput)
        stringPowerStatus = powerStatus.group(1)
        print('Server'+stringPowerStatus)
    finally:
        if ssh:
            ssh.close()
    return 'Server'+stringPowerStatus

def hpServerOn():
    ssh = None
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(iloIpAddress, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command('POWER on')
        ouput = str(stdout.read())
        #print (ouput)
        powerStatus = re.search('Server(.*)\\.', ouput)
        stringPowerStatus = powerStatus.group(1)
        print('Server'+stringPowerStatus)
    finally:
        if ssh:
            ssh.close()
    return 'Server'+stringPowerStatus

def hpServerOff():
    ssh = None
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(iloIpAddress, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command('POWER off')
        ouput = str(stdout.read())
        #print (ouput)
        powerStatus = re.search('Server(.*)\\.', ouput)
        stringPowerStatus = powerStatus.group(1)
        print('Server'+stringPowerStatus)
    finally:
        if ssh:
            ssh.close()
    return 'Server'+stringPowerStatus

def on_message_powerMangement(client, userdata, message):
    print("%s %s" % (message.topic, message.payload))
    if  (b'off' in message.payload):
        payloadResponse = hpServerOff()
        publish.single(powerManagementStatusTopic, payloadResponse, hostname=mqttHostName)
    else:
        payloadResponse = hpServerOn()
        publish.single(powerManagementStatusTopic, payloadResponse, hostname=mqttHostName)

def statusReporting():
    payloadResponse = hpServerStatus()
    publish.single(publishStatusTopic, payloadResponse, hostname=mqttHostName)
    print(payloadResponse)
    payloadResponse = time.ctime() 
    publish.single(publishStatusTimeTopic, payloadResponse, hostname=mqttHostName)
    print(payloadResponse)
    threading.Timer(10, statusReporting).start()


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.user_data_set([])
mqttc.connect(mqttHostName)
#start reporting
statusReporting()
#subscribe to commands to start and shutdown the server
subscribe.callback(on_message_powerMangement, powerManagementRequestTopic, hostname=mqttHostName)
#loop forever
mqttc.loop_forever()
