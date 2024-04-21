
from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import pad, unpad
'''
def pad(s):
    return s + ((16 - len(s) % 16) * '{')

cipher = Blowfish.new("key must be 4 to 56 bytes".encode(),mode=Blowfish.MODE_CBC)


infile = open("a1.txt", 'rb')
outfile = open("a2.txt", 'wb')
data = infile.read()
infile.close()

encrypted_data = cipher.encrypt(pad(data))
print(encrypted_data)
cipher = Blowfish.new("key must be 4 to 56 bytes".encode(),mode=Blowfish.CBC)
decrypt = cipher.decrypt(encrypted_data)

outfile.write(decrypt)
outfile.close()
'''


from Crypto.Cipher import Blowfish
from struct import pack

infile = open("BFish.py", 'rb')
outfile = open("a2.txt", 'wb')
plaintext = infile.read()
infile.close()

bs = Blowfish.block_size
key = b'An arbitrarily long key'
cipher = Blowfish.new(key, Blowfish.MODE_CBC)

plen = bs - len(plaintext) % bs
padding = [plen]*plen
padding = pack('b'*plen, *padding)
msg = cipher.iv + cipher.encrypt(plaintext + padding)


cipher = Blowfish.new(key, Blowfish.MODE_CBC)
decrypt = unpad(cipher.decrypt(msg),8)
outfile.write(decrypt)
outfile.close()
'''
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import Blowfish
from Crypto.Random import get_random_bytes
data = b'Unaligned'   # 9 bytes
bs = Blowfish.block_size
key = b'An arbitrarily long key'

cipher1 = Blowfish.new(key, Blowfish.MODE_CBC)
ct = cipher1.encrypt(pad(data, 16))

cipher2 = Blowfish.new(key, Blowfish.MODE_CBC)
pt = unpad(cipher2.decrypt(ct), 16)

print(pt)
'''














