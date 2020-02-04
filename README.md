# PyKDumper

**PykDumper** is mimimkatz inspired PyKD based script that retrieves and decrypt usernames,logonservers and credentials from the lsass process.
* PyKDumper2.py supports Python2
* PyKDumper3.py supports Python3

## Requirements 

* Python2.7 OR Python3.6 x64 on Windows (is preferred to have a single Python version installed)
* PyKD x64
* PyDes
* WinDbg :)


## Features

* Dumps user infos + credentials from lsass
* A friendly guide to setup x64 PyKD

## To do:
* AES support
* further PyKD automation

## Installation and Setup 
We are going to cover only Py3 setup here, as Py2 is dead.
1. Download the latest PyKD x64 dll version [here](https://githomelab.ru/pykd/pykd-ext/-/wikis/Downloads) and copy it to:
     ```
     C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\winext
     ```
2. Verify that you can load it from windbg by getting a similar output (depending on version)

   ```
   0: kd> .load pykd
   0: kd> !py
   Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)] on win32
   Type "help", "copyright", "credits" or "license" for more information.
   (InteractiveConsole)
   >>> 
   ```
   Make sure that the python interpreter loaded is also x64.

3. Install the pyKD python module by doing the following:

   ```
   C:\>python pip install pykd
   ```

4. I had some issues integrating the standard pycrypto module together with PyKD, so I decided to use only what I needed for thi PoC, a 3DES library, which can be installed as follows:

   ```
   C:\>python pip install pyDes
   ```

5. Remember to import pykd in your script
   ```python
   import pykd

   print pykd.dbgCommand("!process 0 0 lsass.exe")
   [...]
   ```
 
6. If everything is correctly setup, then you can call the script from within windbg:
   ```
   0: kd> .load pykd
   0: kd> !py <path to script.py>
   ```
   
 ## Sample Output
 ![alt text](https://www.matteomalvica.com/img/lsass/output.png)
   
 ## Reference
 https://www.matteomalvica.com/blog/2020/01/20/mimikatz-lsass-dump-windg-pykd/
