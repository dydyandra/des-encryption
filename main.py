from pydoc import plain
import des_utils, des_materials

BLOCK_SIZE = 64

# generate 16 key untuk 16 round
def getKeysforRound(key):

    # apply permutation with pc1 for 56 bits
    key = des_utils.permutate(key, des_materials.pc1, 56)

    # split key into left and right halves 
    l_key = key[0:28]
    r_key = key[28:56]
    subkeys = []

    # apply 16 iterations for keys
    for i in range(0,16):
        # left shift keys
        l_key = des_utils.l_shift(l_key, des_materials.shifts[i])
        r_key = des_utils.l_shift(r_key, des_materials.shifts[i])

        # combine left and right key to new key
        newKey = l_key + r_key

        # apply permutation with pc2
        key_round = des_utils.permutate(newKey, des_materials.pc2, 48)
        subkeys.append(key_round)
    
    return subkeys


def DES(blockNumber, subkeys):
    print('BLOCK CONTENT', blockNumber)

    # applying initial permutation 
    blockNumber = des_utils.permutate(str(blockNumber), des_materials.ip, 64)
    print('INITIAL PERMUTATION', blockNumber)

    # get Lo and Ro 
    left = blockNumber[0:32]
    right = blockNumber[32:64]
    nextLeft = ""

    # 16 iterations
    # Ln = Rn-1
    # En = Ln-1 XOR f(Rn-1, Kn)
    for i in range(0,16):
        print()
        print('ROUND', i)
        print('INPUT', f'{left} {right}')
        print('SUBKEY', subkeys[i])

        # Ln = Rn - 1
        nextLeft = right

        # start of function

        #expand bit from 32 bits to 48 bits
        r_expanded = des_utils.permutate(right, des_materials.expansion, 48)
        print('EXPANSION PERMUTATION', r_expanded)

        #XOR output of exampnded with the key Kn
        r_XOR = des_utils.XOR(r_expanded, subkeys[i])
        print('XOR', r_XOR)

        #reduce 48 bits to 32 bits
        # 48 bits --> eight groups of six bits
        # convert to eight groups of 4 bits (32 bits)
        r_reduced = sBox(r_XOR)
        print('S-BOX SUBSTITUTION', r_reduced)

        # permutate with permutation map
        r_permute = des_utils.permutate(r_reduced, des_materials.permutationMap, 32)
        print('P-BOX PERMUTATION', r_permute)

        #Ln-1 XOR f(Rn-1, Kn)
        r_final = des_utils.XOR(left, r_permute)
        print('XOR', r_final)
        print('SWAP', f'{right} {r_final}')

        # for the next iteration
        right = r_final
        left = nextLeft 
        output = left + right
        print('OUTPUT', output)
        

    # final round (reverse order of blocks)
    blockNumber = right + left 

    # apply final permutation (IP-1)
    blockNumber = des_utils.permutate(blockNumber, des_materials.finalPermutationMap, 64)
    return blockNumber

def sBox(right):        
    #Function to reduce 48 bits to 32 bits

    r_reduced = ""
    for subArray in range(0,8):
        # get i row --> represent in base 2 a number in the decimal range 0 to 3
        row= int(right[subArray * 6] + right[subArray * 6 + 5])
        row = des_utils.getDecimal(str(row)) # convert to decimal

        # get j column --> represent in base 2 a decimal number in the range 0 to 15
        column = int(right[subArray * 6 + 1] + right[subArray * 6 + 2] + right[subArray * 6 + 3] + right[subArray * 6 + 4])
        column = des_utils.getDecimal(str(column)) # convert to decimal 

        # map row and column to table of sbox 
        map_matrix = des_materials.sBoxMap[subArray][row][column]

        # turn back into binary
        map_matrix = des_utils.getBinary(map_matrix)
        r_reduced = r_reduced + str(map_matrix)

    return r_reduced



def encrypt(plaintext, key, mode = None, last_block=None):
    # convert key into binary 
    key = des_utils.hex_to_bin(key)

    # convert plaintext to binary
    plaintext = str(des_utils.hex_to_bin(plaintext))

    # pad plaintext based on blocksize
    plaintext = des_utils.pad(plaintext, BLOCK_SIZE)

    # generate 16 subkeys for 16 rounds
    subkeys = getKeysforRound(key)

    ciphertext = ''

    # default ECB mode --> separate plaintext into blocks based on BLOCK_SIZE
    for i in range(0, len(plaintext), BLOCK_SIZE):
        block = (plaintext[i:i+BLOCK_SIZE])
        if mode == "cbc":
            # CBC mode == XOR block with IV 
            block = des_utils.XOR(block, last_block)
            print('CBC BLOCK', block)

        # DES operation
        result = DES(str(block), subkeys)
        if mode == 'cbc':
            last_block = result
        ciphertext += (result)
    return ciphertext

def decrypt(cyphertext, key, mode = None, last_block = None):
    key = des_utils.hex_to_bin(key)
    cyphertext = str(des_utils.hex_to_bin(cyphertext))
    cyphertext = des_utils.pad(cyphertext, BLOCK_SIZE)

    subkeysTemp = getKeysforRound(key)
    subkeys = []
    count = 15

    for i in range(len(subkeysTemp)):
        subkeys.append(subkeysTemp[count])
        count -= 1

    ciphertext = ''
    print(cyphertext)
    for i in range(0, len(cyphertext), BLOCK_SIZE):
        block = (cyphertext[i:i+BLOCK_SIZE])

        result = DES((block), subkeys)

        if mode == "cbc":
            result = des_utils.XOR(result, last_block)
            last_block = block

        ciphertext += (result)
    
    return ciphertext


if __name__ == "__main__":
    
    choice = ""
    while choice != 'EXIT':
        choice = input("\n1.Input manually(Hex)\n2.From File (hex)\n3.From File (ASCII)\nInsert choice:")
        if int(choice) == 1:
            ciphertype= int(input("\nEncryption/Decryption Menu:\n1. Enkripsi\n2. Dekripsi\nInsert 1/2:"))
            if ciphertype == 1:
                mode = input("\nInsert mode of encryption (ECB/CBC):")
                if mode.lower() == 'cbc':
                    # insert initialization vector
                    iv = input("\nInsert IV:")

                    #convert to binary
                    last_block = des_utils.hex_to_bin(iv)

                key = input("\nInsert key:")
                plaintext = input("\nInsert Plaintext (HEX):")

                if mode.lower() == 'cbc':
                    ciphertext = encrypt(plaintext, key, mode.lower(), last_block)
                else:
                    ciphertext = encrypt(plaintext, key, mode.lower())
                    
                # convert binary to hex for result
                ciphertext = des_utils.bin_to_hex(ciphertext)
                print("\n\nENCRYPTED: ", ciphertext)

            elif ciphertype == 2:
                mode = input("\nInsert mode of decryption (ECB/CBC):")
                if mode.lower() == 'cbc':
                    iv = input("\nInsert IV:")
                    last_block = des_utils.hex_to_bin(iv)

                key = input("\nInsert key:")
                plaintext = input("\nInsert Ciphertext (HEX):")

                if mode.lower() == 'cbc':
                    plaintext = decrypt(plaintext, key, mode.lower(), last_block)
                else:
                     plaintext = decrypt(plaintext, key, mode.lower())
                    
                plaintext = des_utils.bin_to_hex(plaintext)
                print("\n\nDECRYPTED: ", plaintext)


        elif int(choice) == 2:

            ciphertype= int(input("\nEncryption/Decryption Menu:\n1. Enkripsi\n2. Dekripsi\nInsert 1/2:"))
            if ciphertype == 1:
                mode = input("\nInsert mode of encryption (ECB/CBC):")
                if mode.lower() == 'cbc':
                    iv = input("\nInsert IV:")
                    last_block = des_utils.hex_to_bin(iv)

                keyfile = input("\nInsert filename with key:")
                file = input("\nInsert filename with HEX plaintext:")

                # read file
                key = des_utils.get_file(keyfile)
                plaintext = des_utils.get_file(file)

                if mode.lower() == 'cbc':
                    ciphertext = encrypt(plaintext, key, mode.lower(), last_block)
                else:
                    ciphertext = encrypt(plaintext, key, mode.lower())
                    
                ciphertext = des_utils.bin_to_hex(ciphertext)

                # write to file
                output_file = des_utils.write_file(file, ciphertext)

            elif ciphertype == 2:
                mode = input("\nInsert mode of decryption (ECB/CBC):")
                if mode.lower() == 'cbc':
                    iv = input("\nInsert IV:")
                    last_block = des_utils.hex_to_bin(iv)

                keyfile = input("\nInsert filename with key:")
                file = input("\nInsert filename with HEX ciphertext:")

                key = des_utils.get_file(keyfile)
                ciphertext = des_utils.get_file(file)

                if mode.lower() == 'cbc':
                    plaintext = decrypt(ciphertext, key, mode.lower(), last_block)
                else:
                     plaintext = decrypt(ciphertext, key, mode.lower())
                    
                plaintext = des_utils.bin_to_hex(plaintext)
                output_file = des_utils.write_file(file, plaintext)

        
        elif int(choice) == 3:
            ciphertype= int(input("\nEncryption/Decryption Menu:\n1. Enkripsi\n2. Dekripsi\nInsert 1/2:"))
            if ciphertype == 1:
                mode = input("\nInsert mode of encryption (ECB/CBC):")
                if mode.lower() == 'cbc':
                    iv = input("\nInsert IV:")
                    last_block = des_utils.hex_to_bin(iv)

                keyfile = input("\nInsert filename with key:")
                file = input("\nInsert filename:")

                # read file
                key = des_utils.get_file(keyfile)
                plaintext = des_utils.get_file_hex(file)

                if mode.lower() == 'cbc':
                    ciphertext = encrypt(plaintext, key, mode.lower(), last_block)
                else:
                    ciphertext = encrypt(plaintext, key, mode.lower())
                    
                ciphertext = des_utils.bin_to_str(ciphertext)

                # write to file
                output_file = des_utils.write_file_hex(file, ciphertext)

            elif ciphertype == 2:
                mode = input("\nInsert mode of decryption (ECB/CBC):")
                if mode.lower() == 'cbc':
                    iv = input("\nInsert IV:")
                    last_block = des_utils.hex_to_bin(iv)

                keyfile = input("\nInsert filename with key:")
                file = input("\nInsert filename:")

                key = des_utils.get_file(keyfile)
                ciphertext = des_utils.get_file_hex(file)

                if mode.lower() == 'cbc':
                    plaintext = decrypt(ciphertext, key, mode.lower(), last_block)
                else:
                     plaintext = decrypt(ciphertext, key, mode.lower())
                    
                plaintext = des_utils.bin_to_str(plaintext)
                output_file = des_utils.write_file_hex(file, plaintext)

        else:
            break



    





