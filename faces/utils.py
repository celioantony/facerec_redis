from facerec_redis.settings import REDIS_CONN
import numpy as np
import base64

client = REDIS_CONN

def to_redis(array):
    sep = base64.b64encode(bytes('|', 'utf-8'))
    arr_dtype = bytes(str(array.dtype), 'utf-8')
    encoded = arr_dtype + sep + array.tobytes()
    
    return encoded


def from_redis(hkey, mapkey):
    value = client.hget(hkey, mapkey)
    bdtype, encoded = value.split(b'fA==')
    dtype = bdtype.decode('utf-8')
    nparray = np.frombuffer(encoded, dtype=dtype)
    
    return nparray


def bytes_to_nparray(benc):
    bdtype, encoded = benc.split(b'fA==')
    dtype = bdtype.decode('utf-8')
    nparray = np.frombuffer(encoded, dtype=dtype)
    
    return nparray