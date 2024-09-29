# This program outputs 16-byte, 32-byte, ..., 16k-byte, 32k-byte chunks. The 16k-byte and 32-byte chunks were manually
# copy and pasted into write.py, which produces an incomplete but readable flag5.bmp.

import itertools

from pwn import *

first = b"\x42\x4d\x36\xf8\x00\x00\x00\x00\x00\x00\x36\x00\x00\x00\x28\x00"
second = b"\x00\x00\xf0\x01\x00\x00\x20\x00\x00\x00\x01\x00\x20\x00\x00\x00"
third = b"\x00\x00\x00\xf8\x00\x00\xc4\x0e\x00\x00\xc4\x0e\x00\x00\x00\x00"


def int_to_bmp(b: int):
    # Convert to bmp values
    to_send = b""
    for bb in range(16):
        to_send += b"\xff" if b >> bb & 1 else b"\x00"

    # Note bb = 3 represents b"\x00\x00...\x00\xff\xff"
    return to_send[::-1]


# Get present 16-byte chunks
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect(("challs.pwnoh.io", 13420))
#
#     print("RECEIVED:", s.recv(4096))
#
#     for b1 in range(1, 256):
#         for b2 in range(256):
#             first = b"\x42\x4d\x36??\x00\x00\x00\x00\x00\x36\x00\x00\x00\x28\x00"
#             first = first[:3] + int.to_bytes(b2) + int.to_bytes(b1) + first[5:]
#             assert len(first) == 16
#             first = base64.b64encode(first) + b"\n"
#
#             second = b"\x00\x00??\x00\x00\x20\x00\x00\x00\x01\x00\x20\x00\x00\x00"
#             second = second[:2] + int.to_bytes(b2) + int.to_bytes(b1) + second[4:]
#             assert len(second) == 16
#             second = base64.b64encode(second) + b"\n"
#
#             s.send(second)
#
#     unique_chunks = []
#     chunk_cnt = 0
#     with open("output.txt", "w") as f:
#     for b in range(2 ** 16):
#         s.sendall(base64.b64encode(int_to_bmp(b)) + b"\n")
#
#         if b % 1000 == 999 or b == 2 ** 16 - 1:
#             print("ITERATION", b)
#
#             time.sleep(0.5)
#
#             received = s.recv(1073741824).decode("utf-8").split("\n")
#             print("LEN RECEIVED:", len(received))
#
#             for line in received:
#                 if "chunks" in line:
#                     if "0 chunks" in line:
#                         unique_chunks.append(chunk_cnt)
#                     chunk_cnt += 1
#                 f.write(line)
#                 f.write("\n")

# print(unique_chunks)

# Repeatedly combine chunks
buffer_time = 0.5

unique_chunks = [0, 3, 63, 1023, 16380, 16383, 49152, 50175, 64512, 64515, 64575, 65472, 65475, 65532, 65535]

unique_chunks = list(map(int_to_bmp, unique_chunks))
unique_chunks.append(first)
unique_chunks.append(second)
unique_chunks.append(third)
print(unique_chunks)
with open("output-bigger.txt", "w") as f:
    len_chunk = 32
    while unique_chunks:
        # Restart connection to avoid 2 mb limit
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("challs.pwnoh.io", 13420))
        time.sleep(buffer_time / 5)
        s.recv(4096)

        print("BRUTE FORCING", len_chunk, "-byte chunks")

        nxt_unique_chunks = []
        chunk_cnt = 0

        product = list(itertools.product(unique_chunks, unique_chunks))

        repeat = math.isqrt(len(product))

        for i, (a, b) in enumerate(product):
            s.sendall(base64.b64encode(a + b) + b"\n")

            if i % repeat == repeat - 1 or i == len(product) - 1:
                print("ITERATION", i)

                time.sleep(buffer_time)

                received = ["fck"]
                while chunk_cnt - 1 < i:
                    received = s.recv(1073741824).decode("utf-8").split("\n")
                    while received[-1].strip() != ">>>":
                        print("BAD")
                        received.extend(s.recv(1073741824).decode("utf-8").split("\n"))

                    for line in received:
                        if "chunks" in line:
                            if "0 chunks" in line:
                                nxt_unique_chunks.append(chunk_cnt)
                            chunk_cnt += 1

                if chunk_cnt - 1 != i:
                    print(received[-1])
                    print(chunk_cnt, i)
                    assert chunk_cnt - 1 == i

                # Avoid 2 mb limit
                s.close()
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(("challs.pwnoh.io", 13420))
                time.sleep(buffer_time / 5)
                s.recv(4096)

        print("LEN", len(nxt_unique_chunks))
        print("NXT UNIQUE CHUNKS", nxt_unique_chunks)
        print("SAMPLE:", product[nxt_unique_chunks[-1]][0] + product[nxt_unique_chunks[-1]][1])

        unique_chunks = list(product[i][0] + product[i][1] for i in nxt_unique_chunks)
        f.write(str(unique_chunks))
        f.write("\n")

        s.close()

        len_chunk <<= 1

    print(unique_chunks)
