#strings flagwatch.exe then get those (see pic)


encrypted_flag = [62,63,40,58,39,40,111,63,52,50,53,63,104,48,48,37,3,61,3,55,57,37,48,108,59,59,111,46,33]
decrypted_flag = ''

for num in encrypted_flag:
    decrypted_flag += chr(num ^ 92)  # XOR with 92 and convert to character

print(decrypted_flag)
