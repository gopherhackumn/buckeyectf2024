# Just add another block to the end
# Flag is bctf{e7ym0l0gy_f4c7_7h3_w0rd_hash_c0m35_fr0m_7h3_fr3nch_hacher_wh1ch_m34n5_t0_h4ck_0r_ch0p}

from pwn import *
from Crypto.Cipher import AES
from hashbrown import pad, aes

# p = process(["python", "hashbrown.py"])
p = remote("challs.pwnoh.io", 13419)

print(p.recvline().decode())
p.recvline().decode()
print(p.recvline().decode())
my_message_hex = p.recvline().decode()
my_message = bytes.fromhex(my_message_hex)
print(p.recvline().decode())
signature_hex = p.recvline().decode()
print(p.recvline().decode())

# This is the last state
signature = bytes.fromhex(signature_hex) # 16 byts

# Try to add another state to it
print (len(my_message) % 16)

aug_msg = pad(my_message)

aug_frenchfry = pad(b"french fry")

new_message = aug_msg + b"french fry"

sig2 = aes(aug_frenchfry, signature)
# print(sig2.hex())

print(p.recv().decode())
p.sendline(new_message.hex())
print(p.recv().decode())
p.sendline(sig2.hex())
print(p.recv().decode())
print(p.recv().decode())

