import sys
import struct

def left_rotate(n, b):
    "Left rotate a 32-bit integer n by b bits."
    return ((n << b) | (n >> (32 - b))) & 0xffffffff

def sha640(data):
    "Compute the extended SHA-1 hash (320-bit) of the given data."
    # Initialize variables (extended to 10 values instead of 5)
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0
    h5 = 0x76543210
    h6 = 0xFEDCBA98
    h7 = 0x89ABCDEF
    h8 = 0x01234567
    h9 = 0x3C2D1E0F

    # Pre-processing
    original_byte_len = len(data)
    original_bit_len = original_byte_len * 8

    # Append the bit '1' to the message
    data += b'\x80'

    # Append 0 <= k < 1024 bits '0', so that the resulting message length (in bits)
    # is congruent to 896 (mod 1024)
    while (len(data) * 8) % 1024 != 896:
        data += b'\x00'

    # Append original length in bits at the end of the buffer
    data += struct.pack('>Q', original_bit_len)

    # Process the message in successive 1024-bit chunks
    for i in range(0, len(data), 128):
        w = [0] * 160
        chunk = data[i:i+128]
        
        # Break chunk into thirty-two 32-bit big-endian words w[i], 0 ≤ i ≤ 31
        for j in range(16):
            w[j] = struct.unpack('>I', chunk[j*4:j*4+4])[0]
        
        # Extend the thirty-two 32-bit words into one hundred sixty 32-bit words:
        for j in range(16, 160):
            w[j] = left_rotate(w[j-6] ^ w[j-16] ^ w[j-29] ^ w[j-30], 1)
        
        # Initialize hash value for this chunk
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        f = h5
        g = h6
        h = h7
        i = h8
        j = h9
        
        # Main loop
        for k in range(160):
            if 0 <= k <= 39:
                func = (b & c) | ((~b) & d)
                constant = 0x5A827999
            elif 40 <= k <= 79:
                func = b ^ c ^ d
                constant = 0x6ED9EBA1
            elif 80 <= k <= 119:
                func = (b & c) | (b & d) | (c & d)
                constant = 0x8F1BBCDC
            elif 120 <= k <= 159:
                func = b ^ c ^ d
                constant = 0xCA62C1D6
            
            temp = (left_rotate(a, 5) + func + e + constant + w[k]) & 0xffffffff
            e = d
            d = c
            c = left_rotate(b, 30)
            b = a
            a = temp
            
            temp = (left_rotate(f, 5) + func + j + constant + w[k]) & 0xffffffff
            j = i
            i = h
            h = left_rotate(g, 30)
            g = f
            f = temp
        
        # Add this chunk's hash to result so far
        h0 = (h0 + a) & 0xffffffff
        h1 = (h1 + b) & 0xffffffff
        h2 = (h2 + c) & 0xffffffff
        h3 = (h3 + d) & 0xffffffff
        h4 = (h4 + e) & 0xffffffff
        h5 = (h5 + f) & 0xffffffff
        h6 = (h6 + g) & 0xffffffff
        h7 = (h7 + h) & 0xffffffff
        h8 = (h8 + i) & 0xffffffff
        h9 = (h9 + j) & 0xffffffff
    
    # Produce the final hash value (big-endian) as a 320 bit number:
    return '{:08x}{:08x}{:08x}{:08x}{:08x}{:08x}{:08x}{:08x}{:08x}{:08x}'.format(h0, h1, h2, h3, h4, h5, h6, h7, h8, h9)

message = sys.argv[1].encode("utf-8")
hash_result = sha640(message)
print(hash_result)