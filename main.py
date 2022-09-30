## Fichier de génération du wallet

import secrets, hashlib

SEED_LENGTH = 128


print('Programm starting --------------------------------------------')

### FONCTIONS

def SeedGenerator():
    return secrets.randbits(SEED_LENGTH)


def getGoodSeed():
    binarySeed = 0
    while len(str(binarySeed)) != 130:
        seed = SeedGenerator()
        binarySeed = bin(seed)
    return seed, binarySeed[2:]

def getSlice(seedC):
    slicedTab = []
    pointertab =0
    for i in range(0, 12):
        
        slicedTab.append(seedChecksum[pointertab:pointertab+11])
        pointertab+=11

    return slicedTab


### MAIN


seed, binarySeed = getGoodSeed()
print("\nSeed en binaire :")
print(binarySeed)

hashedSeed = hashlib.sha256(seed.to_bytes(SEED_LENGTH, 'big')).hexdigest()
print("\nSeed hashée :")
print(hashedSeed)

hashedSeedToBin = bin(int(hashedSeed, 16))
fourBytes = str(hashedSeedToBin)[2:6]
print("\n4 Bits :")
print(fourBytes)

seedChecksum = str(binarySeed)+str(fourBytes)
print(seedChecksum)
print(len(seedChecksum))


tab = getSlice(seedChecksum)
print('\n')
print(tab)








