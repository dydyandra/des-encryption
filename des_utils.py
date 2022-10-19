import binascii
import math

def permutate(number, pmap, bits):
    permuteNum = ''
    for i in range(0, bits):
        permuteNum = permuteNum + number[pmap[i] - 1]
        
    return permuteNum

def hex_to_bin(hex):
    bin = int(hex, 16)
    bin = format(bin, "b").zfill(len(4*hex))
    return bin

def bin_to_hex(text):
    text_in_bin = int(text, 2)
    for_pad = math.floor(len(text) / 4)
    return f'{text_in_bin:0{for_pad}X}'


def l_shift(value, num_of_shift):    
    shifted_value = ''
    for i in range(num_of_shift):
        for j in range(1, len(value)):
            shifted_value = shifted_value + value[j]

        shifted_value = shifted_value + value[0]
        value = shifted_value
        shifted_value = ''

    return value

def getBinary(binaryNum):
    return bin(binaryNum).replace("0b", "").zfill(4)

def getDecimal(binaryNum):
    converted = int(binaryNum, 2)
    return converted

def XOR(x, y):
    newRight = ''
    for i in range(len(x)):
        if x[i] == y[i]:
            newRight = newRight + "0"
        else:
            newRight = newRight + "1"

    return newRight

def pad(bin_str, BLOCK_SIZE):
    return bin_str + '0' * ((BLOCK_SIZE - len(bin_str) % BLOCK_SIZE) % BLOCK_SIZE)

def get_file(file):
    with open(file, 'rb') as f:
        text = f.read()
        f.close()
        text = text.decode('ISO-8859-1')
    return text

def write_file(file, text):
    filename = 'output_' + file
    text = text.encode('ISO-8859-1')
    with open(filename, 'wb') as f:
        f.write(text)
        f.close()
    return 1

def bin_to_str(bin):
    return ''.join(chr(int(bin[i:i+8],2)) for i in range(0,len(bin),8))

def get_file_hex(file):
    with open(file, 'rb') as f:
        text = f.read().hex()
        f.close()
        # text = text.decode('ISO-8859-1')
    return text

def write_file_hex(file, text):
    filename = 'output_' + file
    with open(filename, "wb") as fd_out:
        text = text.rstrip('\x00').encode('ISO-8859-1')
        fd_out.write(text)
        fd_out.close()
    return 1








