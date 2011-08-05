import math
from jarray import array
from java.lang.Integer import toString as itos

def decode(s, base):
  n = int(math.ceil(math.log(256, base)))
  bytes = [_stb(''.join(s[i:i+n]),base) for i in xrange(0,len(s),n)]
  return array(bytes, 'b')
  
def encode(bytes, base):
  return ''.join([_bts(b, base) for b in bytes]) 

def _bts(b, base):
  # byte to string, apply 2's compliment if negative
  n = int(math.ceil(math.log(256, base)))
  s = str(itos((abs(b) ^ 0xff) + 0x01 if b < 0 else b, base))
  return s.rjust(n, '0')
  
def _stb(s, base):
  # string to byte, apply 2's compliment if > 128
  i = int(s,base)
  return -1*((i ^ 0xff) + 0x01) if i > 128 else i

