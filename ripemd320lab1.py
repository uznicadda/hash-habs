import ctypes

lib = ctypes.CDLL("./librmd320.so")
lib.ripemd320_c.argtypes = [ctypes.c_char_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_uint8)]
lib.ripemd320_c.restype = None

def ripemd320(message: str) -> str:
    msg_bytes = message.encode('utf-8')
    out = (ctypes.c_uint8 * 40)()
    lib.ripemd320_c(msg_bytes, len(msg_bytes), out)
    return bytes(out).hex()
