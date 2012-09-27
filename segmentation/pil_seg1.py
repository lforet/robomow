from PIL import Image
import pymeanshift as pms

import numpy
import Image

def PIL2array(img):
    return numpy.array(img.getdata(),
                    numpy.uint8).reshape(img.size[1], img.size[0], 3)

def array2PIL(arr, size):
    mode = 'RGBA'
    arr = arr.reshape(arr.shape[0]*arr.shape[1], arr.shape[2])
    if len(arr[0]) == 3:
        arr = numpy.c_[arr, 255*numpy.ones((len(arr),1), numpy.uint8)]
    return Image.frombuffer(mode, size, arr.tostring(), 'raw', mode, 0, 1)

def segment_img(original_image, spatial_radius=5,range_radius=5, min_density=60):
	(segmented_image, labels_image, number_regions) = pms.segment(original_image, spatial_radius, 
                                                              range_radius, min_density)


original_image = Image.open("/home/lforet/images/class1/1.grass3.jpg")


(segmented_image, labels_image, number_regions) = pms.segment(original_image, spatial_radius=10, 
                                                              range_radius=10, min_density=60)
original_image.show()

array2PIL(segmented_image, original_image.size).show()
