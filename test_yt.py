import binascii
import secrets, hashlib

BITS = 128

# Functions

def getFileWords():
    index_list = []
    with open("bip-39Words.txt", "r", encoding='utf-8') as file:
        for word in file.readlines():
            index_list.append(word.strip())
    return index_list

def getMnemonicPhrase(bin_result, index_list):
    wordlist = []
    for i in range(len(bin_result) // 11):

        index = int(bin_result[i*11 : (i+1)*11], 2)
        wordlist.append(index_list[index])
    return wordlist

# Main


entropy_bytes = secrets.token_bytes(16)
print('entropy: '+ str(entropy_bytes))
hex_entropy = entropy_bytes.hex()
print("\nHex_entropy : \n" + hex_entropy)

hashed_entropy = hashlib.sha256(entropy_bytes).hexdigest()
print("\nHashed_entropy : \n" + hashed_entropy)

print('\n')

bin_result = (
    bin(int(hex_entropy, 16))[2:].zfill(BITS)
    + bin(int(hashed_entropy, 16))[2:].zfill(BITS)[:4]
)

print('\nBin result: ' + str(bin_result))
# print(len(bin_result))

index_list = getFileWords()
wordlist = getMnemonicPhrase(bin_result, index_list)

print(len(wordlist))
phrase = " ".join(wordlist) 
print(phrase)

def master_private(root_seed_bytes):
    hmac_seed_out=bin(int(hashlib.sha512(root_seed_bytes).hexdigest(),16))
    print(len(hmac_seed_out))
    left_root=hmac_seed_out[2:258].zfill(256)
    master_chain_code=hmac_seed_out[258:].zfill(256)
    return left_root,master_chain_code

# print(int(bin_result))

# a,b = master_private(bytes([int(i) for i in bin_result]))
# print("\nMaster Private key : ",end='')
# print(a)
# print(len(a))
# print("\nMaster Chain Code : ",end='')
# print(b)
# print(len(b))