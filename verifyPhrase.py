import secrets, hashlib, binascii


# Functions

def getFileWords():
    index_list = []
    with open("bip-39Words.txt", "r", encoding='utf-8') as file:
        for word in file.readlines():
            index_list.append(word.strip())
    return index_list

def wordToInt(phrase, index_list):
    intTab = []
    
    for word in phrase.split(' '):
        for i in range(len(index_list)):
            if word == index_list[i]:
                intTab.append(i)
                break

    return intTab

def intToBin(intPhrase):
    binPhrase = ''
    for n in intPhrase:
        binPhrase += str(bin(n)[2:].zfill(11))

    return binPhrase

# test 

def verifyBinOutput(bin_result, index_list):
    wordlist = []
  
    bin_result = str(bin_result)
    for i in range(len(bin_result) // 11):
        index = [i*11, (i+1)*11]
        wordInt = int(bin_result[index[0] : index[1]], 2)
        wordlist.append(index_list[wordInt])
    return wordlist

# Main

phrase = input("Please type your 12 words passPhrase : ")


index_list = getFileWords()
intPhrase = wordToInt(phrase, index_list)
print('\nInt phrase :')
print(intPhrase)

binPhrase = intToBin(intPhrase)
print('\nBinary Phrase :\n'+str(binPhrase))
print('\nlen binPhrase = '+str(len(binPhrase)))

### To check if we get the same word list as entered
# verifyWords = verifyBinOutput(binPhrase, index_list)
# print('\nVerified word list : \n'+ " ".join(verifyWords))

def verifyChecksum(binPhrase):
    phraseChecksum = binPhrase[-4:]
    binPhraseWTChecksum = binPhrase[:-4]
    bytesPhrase = bytes([int(i, 16) for i in binPhraseWTChecksum])
    hashed_bytesPhrase = hashlib.sha256(bytesPhrase).hexdigest()
    print(hashed_bytesPhrase)
    checksum = bin(int(hashed_bytesPhrase, 16))[2:].zfill(128)[:4]
    print(checksum, phraseChecksum)

verifyChecksum(binPhrase)