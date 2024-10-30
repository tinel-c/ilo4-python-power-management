# ilo4-python-power-management


## Instalation documentation

# Install python
```
sudo apt get install python3
```
# Install pip
```
sudo apt install python3-pip -y
```
# Install venv
```
sudo apt install python3.10-venv
```
# Check pip is install
```
pip3 -V
```
# Install python packages
```
sudo python3 -m venv .venv
source .venv/bin/activate
pip install paramiko
pip install paho-mqtt
pip install regex

# Download sourcecode
```
git clone https://github.com/tinel-c/ilo4-python-power-management.git
```

#install it as a service 
Copy ilo4ServerPowerManager.service to /lib/systemd/system/ilo4ServerPowerManager.service

```
sudo cp ilo4ServerPowerManager.service /lib/systemd/system/ilo4ServerPowerManager.service
```

Reload systemd

```
sudo systemctl daemon-reload
sudo systemctl enable ilo4ServerPowerManager.service
sudo systemctl start ilo4ServerPowerManager.service
sudo systemctl status ilo4ServerPowerManager.service
```

