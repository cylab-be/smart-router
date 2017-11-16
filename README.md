# smart-router

[![Build Status](https://travis-ci.org/RUCD/smart-router.svg?branch=master)](https://travis-ci.org/RUCD/smart-router)


# DNS-sniffer
The DNS-sniffier uses the **scapy-python3** lib.
### First tests on DNS-sniffer
DNS answers are stored into the **"smartrouter"** database on the **"DNSQueries"** table.

#### Usage :

```bash
cd /home/vargrant/python
sudo python3.5 dns_sniffer_0.0.py
```
#### or

```bash
sudo /usr/bin/python3.5 /home/vagrant/python/dns_sniffer_0.0.py
```

#### In another shell :

```bash
nslookup nicode.me
nslookup facebook.be
```

### Object Oriented Python
This is a first object oriented version of the sniffer. The **testclass.py** tests the sniffer.
#### Usage :

```bash
cd /home/vargrant/python
sudo python3.5 testclass.py
```

#### or

```bash
sudo /usr/bin/python3.5 /home/vagrant/python/testclass.py
```

# ohmyzsh
For more conviviality, you can install ohmyzsh. A password must be setup before installing ohmyzsh. So you can run : 

```bash
passwd
sh -c "$(wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"
```

	
