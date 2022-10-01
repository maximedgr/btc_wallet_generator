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

# Split the binary phrase into a list of 8 bits numbers, then transform numbers into integers
def binToInt(binPhraseWTChecksum):
    intPhrase = []
    for i in range(len(binPhraseWTChecksum) // 8):
        index = [i*8, (i+1)*8]
        fourBits = binPhraseWTChecksum[index[0] : index[1]]
        intPhrase.append(int(fourBits, 2))
    
    return intPhrase

# Get the binary phrase, then take the 128 first bits,
# then call the above binToInt function,
# then transform the integers into bytes,
# then hash the bytes,
# then get the last 4 bits (checksum) and compare with the phraseChecksum value
def verifyChecksum(binPhrase):
    phraseChecksum = binPhrase[-4:]

    binPhraseWTChecksum = binPhrase[:-4]
    int_phrase = binToInt(binPhraseWTChecksum)
    print('\nInt_phrase: ')
    print(int_phrase)

    bytes_phrase = bytes([i for i in int_phrase])
    print('\nBytes_phrase: ')
    print(bytes_phrase)

    hashed_bytesPhrase = hashlib.sha256(bytes_phrase).hexdigest()
    print('\nHashed_bytesPhrase: ')
    print(hashed_bytesPhrase)

    checksum = bin(int(hashed_bytesPhrase, 16))[2:].zfill(128)[:4]
    print('\nChecksum de la seed entrée : ' + phraseChecksum + ' | Checksum calculé : '+ checksum)
    message = 'Le checksum est VALIDE' if checksum == phraseChecksum else 'Le checksum ne correspond pas'
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

