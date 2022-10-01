import binascii
import secrets, hashlib
from turtle import right

BITS = 128


# Main


entropy_bytes = secrets.token_bytes(16)

hex_entropy = entropy_bytes.hex()
print("\nHex_entropy : \n" + hex_entropy)

hashed_entropy = hashlib.sha256(entropy_bytes).hexdigest()
print("\nHashed_entropy : \n" + hashed_entropy)

entropy_length = len(entropy_bytes)
print(entropy_length)
print('\n')

bin_result = (
    bin(int(hex_entropy, 16))[2:].zfill(128)
    + bin(int(hashed_entropy, 16))[2:].zfill(128)[:4]
)

print('\nBin result: ' + str(bin_result))
print(len(bin_result))

index_list = []
with open("bip-39Words.txt", "r", encoding='utf-8') as file:
    for word in file.readlines():
        index_list.append(word.strip())


wordlist = []
for i in range(len(bin_result) // 11):

    index = int(bin_result[i*11 : (i+1)*11], 2)
    wordlist.append(index_list[index])

print(len(wordlist))
phrase = " ".join(wordlist) 
print(phrase)


# BIP43/44

def master_private(root_seed_bytes):
    hmac_seed_out=bin(int(hashlib.sha512(root_seed_bytes).hexdigest(),16))
    print(len(hmac_seed_out))
    left_root=hmac_seed_out[2:258].zfill(256)
    master_chain_code=hmac_seed_out[258:].zfill(256)
    return left_root,master_chain_code

# print(int(bin_result))

a,b = master_private(bytes([int(i) for i in bin_result]))
print("\nMaster Private key : ",end='')
print(hex(int(a)))
print("\nMaster Chain Code : ",end='')
print(hex(int(b)))
