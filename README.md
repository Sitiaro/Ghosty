# Kik Bot API #

This is a modification to kik-bot-api-unofficial and can be used as a dox tool. It also has an in-build url shortener that uses tinyurl and a ping of death. A ping of death is a type of attack on a system that involves sending a malformed or otherwise malicious ping to the system. In layman terms, its a more simplified dos attack.

The bot uses an updated kik version so you may encounter a captcha while trying to login. 

You can dm me at [@Emouit](https://kik.me/Emouit) on kik if you need help with anything related to this or have any suggestions.

# Features #

### Commands ###

Commands to be entered in a the bot's dms;

```
- .pod <source_ip> <target_ip> <message> <number_of_packets> - ping of death.
- .shorten <url_here> - to shorten a url.
- .ip <ip_address_here> - ip address lookup.
- .name <first_name> <last_name> - name lookup (can give address, etc.)
- .num <10_digit-num here> - phone number lookup.
- .uname <username> - to check a username across various social platforms.
```

*------------------------*

## Installation and dependencies ##

First, make sure you are using **Python 3.6+**, not python 2.7 or python 3.9. Linux follows a different procedure and it's listed below'.


** (Do this before installing the api/more on how to get python 3.8 below.)

If you are using [Termux](https://termux.com/), then use `pkg install libxml2 libxslt` to install `lxml` and `pkg install zlib libpng libjpeg-turbo` to install `pillow` dependencies.

## Installation (this may take a while so be patient) ##
```
$ git clone https://github.com/Sitiaro/Ghosty **
```
```
$ pip install ./Ghosty
```
```
$ cd Ghosty
```
```
$ python requirements.py
```
## Usage ##

(Do **not** use the change directory step if you're already in the working directory, i.e. the Ghosty directory)

```
$ cd Ghosty
```
```
$ python ghosty.py
```
Login with the username and password of your account and type '.help' for a list of commands.


## Replacing python 3.9 with 3.8 ##

**(Termux)**

Uninstall python -
```
$ pkg uninstall python
```
Check the arch of your device cpu using -
```
$ uname -m
```
Go to https://github.com/Termux-pod/termux-pod and find the file corresponding to your device's CPU. You should try python_3.8.6_.deb first and then the static version if there is any error.

Download the raw .deb file corrosponding to your arch and follow the next steps to replace whatever python you have with python 3.8.x.
```
$ cd /sdcard/Download
```
```
$ dpkg -i ./python_3.8.6_<CPU_ARCH.>.deb
```
Once again, replacing <CPU_ARCH.> with your cpu's architecture.


# Adding python 3.8 to Linux #

Head over to https://www.python.org/downloads/release/python-386/ 
Scroll down and download XZ compressed source tarball. Once it finishes download, open your downloads, right click on the compressed python folder, and click extract to > Desktop. Once it finishes, open your terminal and cd to that python directory that's on your desktop. Once you're into that directory, run the following commands one at a time (will take time):
```
$ sudo su 
```
or
```
$ su root
```
(will ask you for your root password, enter it and proceed to the next step)
```
$ ./configure
```
```
$ make install
```
## Installation ## (this may take a while so be patient)
```
$ git clone https://github.com/Sitiaro/Ghosty **
```
```
$ pip3 install ./Ghosty
```
## Usage ##
```
$ cd Ghosty
```
```
$ python3.8 ghosty.py
```
**Login with the username and password of your account and use '.help' for a list of commands.**

