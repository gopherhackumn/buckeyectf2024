c = 0xfe9d88f3d675d0c90d95468212b79e929efffcf281d04f0cfa6d07704118943da2af36b9f8
p = int.from_bytes(b'Blue is greener than purple for sure!')

key = (~c) ^ p

cflag = 0xde9289f08d6bcb90359f4dd70e8d95829fc8ffaf90ce5d21f96e3d635f148a68e4eb32efa4

print(bytes.fromhex(hex(~(key ^ cflag))[2:]))  # bctf{why_xn0r_y0u_b31ng_so_3xclu51v3}
