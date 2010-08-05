from opencv import adaptors
from pygame import surfarray

def surf2CV(surf):
    """Given a surface, convert to an opencv format (cvMat)
    """
    numpyImage = surfarray.pixels3d(surf)
    cvImage = adaptors.NumPy2Ipl(numpyImage.transpose(1,0,2))
    return cvImage

def cv2SurfArray(cvMat):
    """Given an open cvMat convert it to a pygame surface pixelArray
    Should be able to call blit_array directly on this.
    """
    numpyImage = adaptors.Ipl2NumPy(cvMat)
    return numpyImage.transpose(1,0,2)


