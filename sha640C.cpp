#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <iomanip>
#include <cstring>

uint32_t left_rotate(uint32_t n, uint32_t b) {
    return ((n << b) | (n >> (32 - b))) & 0xffffffff;
}

std::string sha640(const std::string& data) {
    uint32_t h0 = 0x67452301;
    uint32_t h1 = 0xEFCDAB89;
    uint32_t h2 = 0x98BADCFE;
    uint32_t h3 = 0x10325476;
    uint32_t h4 = 0xC3D2E1F0;
    uint32_t h5 = 0x76543210;
    uint32_t h6 = 0xFEDCBA98;
    uint32_t h7 = 0x89ABCDEF;
    uint32_t h8 = 0x01234567;
    uint32_t h9 = 0x3C2D1E0F;

    uint64_t original_byte_len = data.size();
    uint64_t original_bit_len = original_byte_len * 8;

    std::vector<uint8_t> padded_data(data.begin(), data.end());
    padded_data.push_back(0x80);

    while ((padded_data.size() * 8) % 1024 != 896) {
        padded_data.push_back(0x00);
    }

    for (int k = 7; k >= 0; --k) {
        padded_data.push_back(static_cast<uint8_t>((original_bit_len >> (k * 8)) & 0xff));
    }

    for (size_t chunk_offset = 0; chunk_offset < padded_data.size(); chunk_offset += 128) {
        uint32_t w[160] = { 0 };
        for (int j = 0; j < 16; ++j) {
            w[j] = (padded_data[chunk_offset + j * 4] << 24) |
                (padded_data[chunk_offset + j * 4 + 1] << 16) |
                (padded_data[chunk_offset + j * 4 + 2] << 8) |
                (padded_data[chunk_offset + j * 4 + 3]);
        }

        for (int j = 16; j < 160; ++j) {
            w[j] = left_rotate(w[j - 6] ^ w[j - 16] ^ w[j - 29] ^ w[j - 30], 1);
        }

        uint32_t a = h0, b = h1, c = h2, d = h3, e = h4;
        uint32_t f = h5, g = h6, h = h7, i = h8, j = h9;

        for (int k = 0; k < 160; ++k) {
            uint32_t func, constant;
            if (k <= 39) {
                func = (b & c) | ((~b) & d);
                constant = 0x5A827999;
            }
            else if (k <= 79) {
                func = b ^ c ^ d;
                constant = 0x6ED9EBA1;
            }
            else if (k <= 119) {
                func = (b & c) | (b & d) | (c & d);
                constant = 0x8F1BBCDC;
            }
            else {
                func = b ^ c ^ d;
                constant = 0xCA62C1D6;
            }

            uint32_t temp = (left_rotate(a, 5) + func + e + constant + w[k]) & 0xffffffff;
            e = d;
            d = c;
            c = left_rotate(b, 30);
            b = a;
            a = temp;

            temp = (left_rotate(f, 5) + func + j + constant + w[k]) & 0xffffffff;
            j = i;
            i = h;
            h = left_rotate(g, 30);
            g = f;
            f = temp;
        }

        h0 = (h0 + a) & 0xffffffff;
        h1 = (h1 + b) & 0xffffffff;
        h2 = (h2 + c) & 0xffffffff;
        h3 = (h3 + d) & 0xffffffff;
        h4 = (h4 + e) & 0xffffffff;
        h5 = (h5 + f) & 0xffffffff;
        h6 = (h6 + g) & 0xffffffff;
        h7 = (h7 + h) & 0xffffffff;
        h8 = (h8 + i) & 0xffffffff;
        h9 = (h9 + j) & 0xffffffff;
    }

    std::stringstream ss;
    ss << std::hex << std::setfill('0');
    ss << std::setw(8) << h0 << std::setw(8) << h1 << std::setw(8) << h2 << std::setw(8) << h3
        << std::setw(8) << h4 << std::setw(8) << h5 << std::setw(8) << h6 << std::setw(8) << h7
        << std::setw(8) << h8 << std::setw(8) << h9;
    return ss.str();
}

int main(int argc, char* argv[]) {
    std::string data = "sha640";

    if (argc != 1) {
        data = argv[1];
    }
    
    std::cout << "SHA-640: " << sha640(data) << std::endl;
    return 0;
}
