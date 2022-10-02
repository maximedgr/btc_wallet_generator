import secrets, hashlib, binascii

####### Functions

# Get the words from the bip39 file in a list
def getFileWords():
    index_list = []
    with open("bip-39Words.txt", "r", encoding='utf-8') as file:
        for word in file.readlines():
            index_list.append(word.strip())
    return index_list

# Transform the words into a list of integers
def wordToInt(phrase, index_list):
    intTab = []
    
    for word in phrase.split(' '):
        for i in range(len(index_list)):
            if word == index_list[i]:
                intTab.append(i)
                break

    return intTab

# Transform a list of integers into a binary result
def intToBin(intPhrase):
    binPhrase = ''
    for n in intPhrase:
        binPhrase += str(bin(n)[2:].zfill(11))

    return binPhrase


# To check if we get the same word list as entered
def verifyBinOutput(bin_result, index_list):
    wordlist = []
  
    bin_result = str(bin_result)
    for i in range(len(bin_result) // 11):
        index = [i*11, (i+1)*11]
        wordInt = int(bin_result[index[0] : index[1]], 2)
        wordlist.append(index_list[wordInt])
    return wordlist

# Get the binary phrase, then take the 128 first bits,
# then transform each 8 bits long parts into bytes,
# then hash the bytes,
# then get the last 4 bits (checksum) and compare with the phraseChecksum value
def verifyChecksum(binPhrase):
    phraseChecksum = binPhrase[-4:]

    binPhraseWTChecksum = binPhrase[:-4]
    bytes_phrase = int(binPhraseWTChecksum, 2).to_bytes(len(binPhraseWTChecksum) // 8, byteorder='big')
    print('\nBytes_phrase: ')
    print(bytes_phrase)

    hashed_bytesPhrase = hashlib.sha256(bytes_phrase).hexdigest()
    print('\nHashed_bytesPhrase: ')
    print(hashed_bytesPhrase)

    checksum = bin(int(hashed_bytesPhrase, 16))[2:].zfill(128)[:4]
    print('\nPassPhrase Checksum : ' + phraseChecksum + ' | Processed Checksum : '+ checksum)
    message = 'The Checksum is valid' if checksum == phraseChecksum else 'ERROR : The Checksum is invalid'
    print(message)

####### Main

def verify_seed():

    phrase = input("Please type your 12 words passPhrase : ")

    index_list = getFileWords()
    intPhrase = wordToInt(phrase, index_list)
    print('\nInt phrase : ')
    print(intPhrase)

    binPhrase = intToBin(intPhrase)
    print('\nBinary Phrase : \n'+str(binPhrase))
    #print('len binPhrase = '+str(len(binPhrase)))

    ### Show the 12 words, To check if we get the same word list as entered
    # verifyWords = verifyBinOutput(binPhrase, index_list)
    # print('\nVerified word list : \n'+ " ".join(verifyWords))

    verifyChecksum(binPhrase)
