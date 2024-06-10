import sys


def sha128(input_string):
    # Initial values (16 characters = 64 bits)
    h1 = 0x12345678
    
    # Prime numbers for mixing
    prime1 = 0x45d9f3b
    
    # Process the input string in chunks of 8 bytes
    for i in range(0, len(input_string), 8):
        chunk = input_string[i:i+8]
        
        # Convert chunk to an integer
        chunk_value = 0
        for c in chunk:
            chunk_value = (chunk_value << 8) + ord(c)
        
        # Mix the chunk with h1 and h2
        h1 = (h1 ^ chunk_value) * prime1
        
        # Ensure the values fit in 32 bits
        h1 = h1 & 0xffffffff
    
    # Convert to hexadecimal and ensure it's 16 characters long
    return f'{h1:008x}'

message = sys.argv[1]
hash_result = sha128(message)
print(hash_result)
