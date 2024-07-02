#include <iostream>
#include <string>
#include <sstream>

std::string sha128(const std::string& input_string) {
    unsigned int h1 = 0x12345678;

    unsigned int prime1 = 0x45d9f3b;

    for (size_t i = 0; i < input_string.length(); i += 8) {
        std::string chunk = input_string.substr(i, 8);

        unsigned int chunk_value = 0;
        for (char c : chunk) {
            chunk_value = (chunk_value << 8) + static_cast<unsigned char>(c);
        }

        h1 = (h1 ^ chunk_value) * prime1;

        h1 = h1 & 0xffffffff;
    }

    std::stringstream result;
    result << std::hex << std::uppercase << std::setfill('0') << std::setw(8) << h1;
    return result.str();
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <message>" << std::endl;
        return 1;
    }

    std::string message = argv[1];
    std::string hash_result = sha128(message);
    std::cout << hash_result << std::endl;

    return 0;
}
