"""
Joseph Lee
Software Design Mini-Project 5
Computational Art
"""

import random
from PIL import Image
import math
import cv2


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    recursion_depth=random.randint(min_depth,max_depth)
    building_blocks_no_params=["x","y"]
    building_blocks_one_param=["cos_pi","sin_pi","x","y"]
    building_blocks_two_params=["prod","avg","cos_pi","sin_pi","x","y"]

    if recursion_depth<=0:
        return [random.choice(building_blocks_no_params)]
    if recursion_depth==1:
        return [random.choice(building_blocks_one_param),build_random_function(min_depth-1,max_depth-1)]
    if recursion_depth>=2:
        return [random.choice(building_blocks_two_params),build_random_function(min_depth-1,max_depth-1),build_random_function(min_depth-1,max_depth-1)]

def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
        >>> evaluate_random_function(['prod',['x'],['y']],.5,-.5)
        -0.25
    """
    if f[0] == 'y':
	    return y
    elif f[0] == 'x':
	    return x
    elif len(f) == 1:
        if f[0] == 'x': 
            return x
        elif f[0] == 'y':
	    	return y

    elif f[0] == 'avg':
        arg = evaluate_random_function(f[1],x,y)
        arg1 = evaluate_random_function(f[2],x,y) 
        return .5*(arg+arg1)

    elif f[0] == 'prod':
        arg = evaluate_random_function(f[1],x,y)
        arg1 = evaluate_random_function(f[2],x,y)        
        return float(arg)*float(arg1)

    elif f[0] == 'cos_pi':
        arg = evaluate_random_function(f[1],x,y)
        return math.cos(math.pi * arg)

    elif f[0] == 'sin_pi':
        arg = evaluate_random_function(f[1],x,y)
        return math.sin(math.pi * arg)


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    output_range = output_interval_end - output_interval_start
    input_range = input_interval_end - input_interval_start
    scaled_input_value = float(val - input_interval_start)/float(input_range)
    return output_interval_start+(scaled_input_value*output_range)

def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    red_function=build_random_function(2, 5)
    green_function=build_random_function(2, 5)
    blue_function=build_random_function(2, 5)
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    """
    I started working on implementing the creation of a movie.  I have not
    introduced the third variable t so the video would be choppy since each
    frame is completely random and not connected to the previous frame in any
    way.  I ran out of time and so I did not finish implementing the movie creation

    """
    num_frames=10
    for frame in range(num_frames):
    	filename="{}.jpg".format(frame)
    	generate_art(filename)
    video = cv2.VideoWriter('video.avi',-1,1,(350,350))
    for i in range(num_frames):
    	img=cv2.imread("{}.jpg".format(i))
    	video.write(img)

cv2.destroyAllWindows()
video.release()
