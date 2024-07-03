#include <iostream>
#include <iomanip>
#include <string>

std::string sha64(const std::string& input_string) {
    uint32_t h1 = 0x12345678;
    uint32_t prime1 = 0x45d9f3b;

    for (size_t i = 0; i < input_string.length(); i += 8) {
        std::string chunk = input_string.substr(i, 8);

        uint32_t chunk_value = 0;
        for (char c : chunk) {
            chunk_value = (chunk_value << 8) + static_cast<uint8_t>(c);
        }

        h1 = (h1 ^ chunk_value) * prime1;

        h1 = h1 & 0xffffffff;
    }

    std::stringstream ss;
    ss << std::hex << std::setw(8) << std::setfill('0') << h1;

    return ss.str();
}

int main(int argc, char* argv[]) {
    std::string data = "sha64";

    if (argc != 1) {
        data = argv[1];
    }
    
    std::cout << sha64(data) << std::endl;
    return 0;
}
