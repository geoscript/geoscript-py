from javax.media.jai import Interpolation

_interp = {}
_interp['nearest'] = Interpolation.INTERP_NEAREST
_interp['bilinear'] = Interpolation.INTERP_BILINEAR
_interp['bicubic'] = Interpolation.INTERP_BICUBIC

def interpolation(name):
  return Interpolation.getInstance(_interp[name])
