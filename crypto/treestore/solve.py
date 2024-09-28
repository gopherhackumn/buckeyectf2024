from pwn import *
from string import *
from make_flag import render
from base64 import *

p = process(["python", "main.py"])

print(p.recv().decode())

flag_chars = ascii_uppercase + ascii_lowercase + "0123456789{}_-"
char_render = dict()

for ch in flag_chars:
    im = render(ch)
    char_render[ch] = im

# Check if a chunk is in the flag
def check_chunk(b: bytes) -> bool:
    p.sendline(b64encode(b))
    line = p.recvline().decode()
    chunks_added = int(line.strip(">>> ").split("chunks were added")[0])
    p.recvline()
    return chunks_added == 1

boundaries = dict()
boundaries_to_letter_pairs = dict()

def store_boundary_between_letters(left, right):
    left_im = char_render[left]
    right_im = char_render[right]

    def half(pix): return b"\xff\xff" if pix[0] else b"\x00\x00"
    def full(pix): return b"\xff\xff\xff\xff" if pix[0] else b"\x00\x00\x00\x00"

    for j in range(32):
        # Comparing (16 bytes left) to (6 bytes left, 10 bytes right)
        # Comparing (4 pixels left) to (1.5 pixels left, 2.5 pixels right)
        arr_left = b"" # This should be 16 pixels
        arr_right = b""

        arr_left += half(left_im.getpixel((10, j))) # Byte -6
        arr_left += full(left_im.getpixel((11, j))) # Byte -5
        arr_left += full(left_im.getpixel((12, j))) # Byte -4
        arr_left += full(left_im.getpixel((13, j))) # Byte -3
        arr_left += half(left_im.getpixel((14, j))) # Byte -2

        arr_right += half(left_im.getpixel((14, j))) # Byte -2
        arr_right += full(left_im.getpixel((15, j))) # Byte -1
        arr_right += full(right_im.getpixel((0, j))) # Byte 0
        arr_right += full(right_im.getpixel((1, j))) # Byte 1
        arr_right += half(right_im.getpixel((2, j))) # Byte 2

        assert len(arr_left) == 16
        assert len(arr_right) == 16

        arr_full = arr_left + arr_right
        if arr_full not in boundaries_to_letter_pairs: boundaries_to_letter_pairs[arr_full] = set()
        boundaries_to_letter_pairs[arr_full].add((left_ch, right_ch))


for left_ch in flag_chars:
    for right_ch in flag_chars:
        store_boundary_between_letters(left_ch, right_ch)

for boundary, pairs in boundaries_to_letter_pairs.items():
    is_in_flag = check_chunk(boundary)
    if is_in_flag:
        print(boundary, is_in_flag, len(pairs))
        for pair in pairs:
            print("-", pair)

print(len(boundaries_to_letter_pairs))

