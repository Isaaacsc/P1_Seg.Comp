def encrypt(msg: str, key: str) -> str:
    msg_len = len(msg)
    key_len = len(key)
    cipher = ""

    j = 0
    for i in range(msg_len):
        j = j % key_len
        c = ord(msg[i]) + ord(key[j]) - 32
        if c >= 127:
            c -= 95
        cipher += chr(c)
        j += 1

    return cipher


def decrypt(cipher: str, key: str) -> str:
    cipher_len = len(cipher)
    key_len = len(key)
    msg = ""

    j = 0
    for i in range(cipher_len):
        j = j % key_len
        c = ord(cipher[i]) - ord(key[j]) + 32
        if c < 32:
            c += 95
        msg += chr(c)
        j += 1

    return msg


msg = input("Enter message: ")
key = input("Enter key: ")

cipher = encrypt(msg, key)
print("Encrypted message:", cipher)

decrypted_msg = decrypt(cipher, key)
print("Decrypted message:", decrypted_msg)


