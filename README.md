# docker-hosts configuration script

Python script that help you to easily configure new domains with your [docker] instance's IP or any custom IP in your host machine.

Automatizing your [docker] setup :)

## Options
```groovy
$ python dockerhostconf.py -h
Usage: dockerhostconf.py [options]

Options:
  -h, --help            show this help message and exit
  -r ROUTE, --route=ROUTE
                        Hosts alternative Path
  -i DMIP, --ip=DMIP    Custom IP address
  -d DOMAINS, --domain=DOMAINS
                        Custom domain or domain, f.e -d
                        mydomain.com,mydomain2.com
  -n DMNAME, --name=DMNAME
                        docker-machine's name to configure, by default docker-
                        machine calls it <default>
  -o                    override strings found in file
```

## Usage with docker
It uses [docker machine] to get it´s IP and configure your `/etc/hosts` file.

### Example

```groovy
$ python dockerhostconf.py -d myDockerDomain.com

[Config]: docker-machine's  IP <192.168.99.100>
DOMAINS
myDockerDomain.com
[Config]: Checking hosts file...
IP <192.168.99.100> is allready assigned to a domain,
do you want to override it? (y/n): y
[Check]: Domain myDockerDomain.com not used ✓
[Config]: Writing files...
Password:
[Write]: Files written...✓
Do you want to create a backup file .old? (y/n): n
[Write]: Restoring permissions...✓

$ cat /etc/hosts
...
192.168.99.100  myDockerDomain.com
```

## Custom IPs
It does not need to be used specifically for [docker]. It can be used to set custom IPs and domains.

### Example

```groovy
$ python dockerhostconf.py -i 192.168.2.1 -d mydomain.com,mydomain2.com
DOMAINS
mydomain.com
mydomain2.com
[Config]: Checking hosts file...
[Check]: IP not used ✓
[Check]: Domain mydomain.com not used ✓
[Check]: Domain mydomain2.com not used ✓
[Config]: Writing files...
Password:
[Write]: Files written...✓
Do you want to create a backup file .old? (y/n): n
[Write]: Restoring permissions...✓

$ cat /etc/hosts
...
192.168.2.1  mydomain.com mydomain2.com
```

## Include the script as alias

```groovy
$ echo "alias dhostconf='python <local file location>/dockerhostconf.py'" >> ~/.bash_profile

# to apply alias
$ source ~/.bash_profile
$ dhostconf -h
Usage: dockerhostconf.py [options]

Options:
  -h, --help            show this help message and exit
  -r ROUTE, --route=ROUTE
                        Hosts alternative Path
  -i DMIP, --ip=DMIP    Custom IP address
  -d DOMAINS, --domain=DOMAINS
                        Custom domain or domain, f.e -d
                        mydomain.com,mydomain2.com
  -n DMNAME, --name=DMNAME
                        docker-machine's name to configure, by default docker-
                        machine calls it <default>
  -o                    override strings found in file
```

[docker machine]:https://docs.docker.com/machine/
[docker]:https://www.docker.com/
