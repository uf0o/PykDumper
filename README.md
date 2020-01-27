# PyKDumper

**PykDumper** is mimimkatz inspired PyKD based script that retrieves and decrypt usernames,logonservers and credentials from the lsass process.

* Python2.7 on Winodws
* PyKD x64
* PyDes
* WinDBG :)


## Features

* Dumps user infos and credentials from lsass
* A 

## Installation and Setup 
1.  Download the latest PyKD x64 dll version [here](https://githomelab.ru/pykd/pykd-ext/-/wikis/Downloads) and copy it to
  
   ```
   C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\winext
   ```
2. Verify that you can load it from windbg by getting a similar output

   ```
   0: kd> .load pykd
   0: kd> !py
   Python 2.7.17 (v2.7.17:c2f86d86e6, Oct 19 2019, 21:01:17) [MSC v.1500 64 bit (AMD64)] on win32
   Type "help", "copyright", "credits" or "license" for more information.
   (InteractiveConsole)
   >>> 
   ```Make sure that the python interpreter loaded is also x64.

3. Install the pyKD python module by doing the following:

   ```
   C:\path\to\corresponding_x64\python.exe -m pip install pykd
   ```

4. I had some issues integrating the standard pycrypto module together with PyKD, so I decided to use only what I needed for thi PoC, a 3DES library, which can be installed as follows:

   ```
   C:\path\to\corresponding_x64\python.exe -m pip install pyDes
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
