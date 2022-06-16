# Previous function used to get and store image pixels in list, took a very long time, has been replaced with optimized alternative
# Takes a path to the image that needs to be stored
# Returns image as matrix, get pixels with pixel_values[x][y]
def get_image(image_path):
    """Get a numpy array of an image so that one can access values[x][y]."""
    image = Image.open(image_path, "r")
    width, height = image.size
    pixel_values = list(image.getdata())
    if image.mode == "RGB":
        channels = 3
    elif image.mode == "L":
        channels = 1
    else:
        print("Unknown mode: %s" % image.mode)
        return None
    pixel_values = np.array(pixel_values).reshape((width, height, channels))
    return pixel_values
    
    
# uses get_image to create and return a list of frame matrices
def create_frames_list(path, frame_count):
    frames = []
    print('Creating frames matrix...')
    for i in range(frame_count):
        frames.append(get_image(path + '/frame%d.jpg' % i))
    print('Done')
    return frames



# get_image() time test with 100 frames, most real cases will have about 500 frames.
def test_get_image():
    images = []
    start = time.time()

    print('Getting Images...')
    for i in range(100):
        images.append(get_image('frames/frame%d.jpg' % i))
        
    end = time.time()
    delta = end - start

    print('Done, took %d seconds' % delta)



# time test with 100 frames, this time using cv2.imread() most real cases will have about 500 frames.
def test_opencv():
    images = []
    start = time.time()

    print('Getting Images...')
    for i in range(100):
        images.append(cv2.imread('frames/frame%d.jpg' % i, 1))
        
    end = time.time()
    delta = end - start

    print('Done, took %d seconds' % delta)
