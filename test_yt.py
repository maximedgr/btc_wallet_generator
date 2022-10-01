import binascii
import secrets, hashlib

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

# print('\nBin result: ' + str(bin_result))
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