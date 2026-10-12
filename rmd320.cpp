#include <cryptopp/ripemd.h>
#include <cstdint>
#include <cstddef>

extern "C" void ripemd320_c(const uint8_t* data, size_t len, uint8_t* digest) {
    CryptoPP::RIPEMD320 hash;
    hash.CalculateDigest(digest, data, len);
}
