try:
    from PIL import Image
except ImportError:
    print("Error: Pillow not installed")


def split_image(image, n = 8):
    """returns n x n pixel blocks of image in a 2D array"""

    if (image.size[0] % n != 0) or (image.size[1] % n != 0):
        print("Image dimensions are not divisible by", n)
        return

    pieces = []

    for j in range(0, image.size[1], n):
        # Iterae through each row of image
        row = []
        
        for i in range(0, image.size[0], n):
            #Iterate through each element in row
            row.append(image.crop((i, j, i+n, j+n)))
        
        pieces.append(row)
    
    return pieces


def stitch_images(pieces, mode = 'L'):
    """returns back image by stiching 2D array of n x n pixel blocks (mode L is black and white)"""

    # width and height of image pieces
    w, h = pieces[0][0].size

    # width and height of resulting image
    width = len(pieces[0]) * w
    height = len(pieces) * h

    # create new image
    image = Image.new(mode, (width, height))

    for j in range(int(height/h)):
        # Iterate through each row
        for i in range(int(width/w)):
            # Iterate through each piece in row
            image.paste(pieces[j][i], (i*w, j*h))
    
    return image


def matrix_to_pixels(matrix, mode = 'L'):
    """converts 2D matrix to image"""

    # 1D array containg data
    data = []
    # Image
    image = Image.new(mode, (len(matrix), len(matrix[0])))

    for i in range(len(matrix)):
        # Iterate through each row
        for j in range(len(matrix[0])):
            # Iterate through each element in row
            data.append(matrix[j][i])
    
    image.putdata(data)
    
    return image
