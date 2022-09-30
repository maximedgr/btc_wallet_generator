import secrets
import hashlib
import sys


### FONCTIONS


def padd_binary(bin_str: str, size: int) -> str:
    """
    Pads a binary string with zeros to the left
    :param bin_str: binary string to pad
    :param size: size of the padded string
    :return: padded binary string
    """
    for _ in range(size - len(bin_str)):
        bin_str = '0' + bin_str
    return bin_str

def byte_to_binary(b: bytes, size: int) -> str:
    """
    Converts a byte to a binary string
    :param byte: byte to convert
    :param size: size of the binary string
    :return: binary string
    """
    order = -1 if sys.byteorder == 'little' else 1
    bin_n = bin(int.from_bytes(b, byteorder='big'))[2:]
    return padd_binary(bin_n, size)

def getSlice(seedC):
    slicedTab = []
    pointertab =0
    for i in range(0, 12):
        
        slicedTab.append(seedC[pointertab:pointertab+11])
        pointertab+=11

    return slicedTab

def SeedToMnemonic(seedChecksum):
    tab = getSlice(seedChecksum)
    # print('\n Lots de 11 bits')
    # print(tab)
    intTab = []
    for cell in tab:
        intTab.append(int(cell, 2))
    
    wordlist = []
    data = []
    file = open("bip-39Words.txt", "r")
    for line in file:
        stripped_line = line.strip()
        line_list = stripped_line.split()
        data.append(line_list[0])

    for cell in intTab:
          
        word = data[cell+1]
        wordlist.append(word)     
        
    return wordlist

### MAIN

entropy_bytes = secrets.token_bytes(128)
# print(entropy_bytes)
entropy = byte_to_binary(entropy_bytes, 128)
# print(entropy)
# print('\n')
hash = hashlib.sha256(entropy_bytes).digest()
entropy_hash = byte_to_binary(hash, 256)
# print(entropy_hash)
seedChecksum = entropy + entropy_hash[:4]

print('Liste de mots : ')
worldList = SeedToMnemonic(seedChecksum)
print(worldList)

for i in worldList:
    print(i, end=' ')



