import sys


def sha64(input_string):
    # Initial values (16 characters = 64 bits)
    h1 = 0x12345678
    h2 = 0x9abcdef0
    
    # Prime numbers for mixing
    prime1 = 0x45d9f3b
    prime2 = 0x41c6ce57
    
    # Process the input string in chunks of 8 bytes
    for i in range(0, len(input_string), 8):
        chunk = input_string[i:i+8]
        
        # Convert chunk to an integer
        chunk_value = 0
        for c in chunk:
            chunk_value = (chunk_value << 8) + ord(c)
        
        # Mix the chunk with h1 and h2
        h1 = (h1 ^ chunk_value) * prime1
        h2 = (h2 ^ chunk_value) * prime2
        
        # Ensure the values fit in 32 bits
        h1 = h1 & 0xffffffff
        h2 = h2 & 0xffffffff
    
    # Combine h1 and h2 to produce the final hash
    final_hash = (h1 << 32) | h2
    
    # Convert to hexadecimal and ensure it's 16 characters long
    return f'{final_hash:016x}'

message = sys.argv[1]
hash_result = sha64(message)
print(hash_result)