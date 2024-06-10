import sys


def sha256(input_string):
    # Initial values (32 characters = 128 bits)
    h1 = 0x12345678
    h2 = 0x9abcdef0
    h3 = 0x0fedcba9
    h4 = 0x87654321
    
    # Custom prime numbers for mixing
    prime1 = 0x1000193
    prime2 = 0x1000187
    prime3 = 0x1000181
    prime4 = 0x100017b
    
    # Process the input string in chunks of 8 bytes
    for i in range(0, len(input_string), 8):
        chunk = input_string[i:i+8]
        
        # Convert chunk to an integer
        chunk_value = 0
        for c in chunk:
            chunk_value = (chunk_value << 8) + ord(c)
        
        # Mix the chunk with h1, h2, h3, and h4
        h1 = (h1 ^ chunk_value) * prime1
        h2 = (h2 ^ chunk_value) * prime2
        h3 = (h3 ^ chunk_value) * prime3
        h4 = (h4 ^ chunk_value) * prime4
        
        # Ensure the values fit in 32 bits
        h1 = h1 & 0xffffffff
        h2 = h2 & 0xffffffff
        h3 = h3 & 0xffffffff
        h4 = h4 & 0xffffffff
    
    # Combine h1, h2, h3, and h4 to produce the final hash
    final_hash = (h1 << 96) | (h2 << 64) | (h3 << 32) | h4
    
    # Convert to hexadecimal and ensure it's 32 characters long
    return f'{final_hash:032x}'

message = sys.argv[1]
hash_result = sha256(message)
print(hash_result)