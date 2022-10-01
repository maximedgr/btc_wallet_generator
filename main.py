import binascii
import secrets, hashlib
from turtle import right

BITS = 128

####### Functions

#Extraction des mots pour la phrase mnemonic - BIP39
def getFileWords():
    index_list = []
    with open("bip-39Words.txt", "r", encoding='utf-8') as file:
        for word in file.readlines():
            index_list.append(word.strip())
    return index_list

#Génération de la phrase mnemonic
def getMnemonicPhrase(bin_result, index_list):
    wordlist = []
    for i in range(len(bin_result) // 11):
        index = int(bin_result[i*11 : (i+1)*11], 2)
        wordlist.append(index_list[index])
    return wordlist

#Génération de la master private key - BIP43/44
def master_private(root_seed_bytes):
    hmac_seed_out=bin(int(hashlib.sha512(root_seed_bytes).hexdigest(),16))
    print(len(hmac_seed_out))
    left_root=hmac_seed_out[2:258].zfill(256)
    master_chain_code=hmac_seed_out[258:].zfill(256)
    return left_root,master_chain_code

####### Main

def main():

    #Génération de generated entropie et du hash associé    
    print("###### Génération d'un wallet BTC : ######\n\n")
    entropy_bytes = secrets.token_bytes(16)
    print('Entropy: '+ str(entropy_bytes))
    hex_entropy = entropy_bytes.hex()
    print("\nHex_entropy : \n" + hex_entropy)

    #Hash via SHA256 de l'entropie
    hashed_entropy = hashlib.sha256(entropy_bytes).hexdigest()
    print("\nHashed_entropy : \n" + hashed_entropy)
    print('\n')

    #Conversion en binaire et ajout checksum à l'entropie
    bin_result = (
        bin(int(hex_entropy, 16))[2:].zfill(BITS)
        + bin(int(hashed_entropy, 16))[2:].zfill(BITS)[:4]
    )
    print('\nBin result: ' + str(bin_result))

    #Création de la phrase mnémonic associée à la seed
    index_list = getFileWords()
    wordlist = getMnemonicPhrase(bin_result, index_list)

    phrase = " ".join(wordlist) 
    print("Mnemonic seed phrase :",end='')
    print(phrase)

    #Master key et Chain Code
    a,b = master_private(bytes([int(i) for i in bin_result]))
    print("\nMaster Private key : ",end='')
    print(hex(int(a)))
    print("\nMaster Chain Code : ",end='')
    print(hex(int(b)))

    #Fin

if __name__== "__main__":
    main()
    print("\n###### End ######\n")

