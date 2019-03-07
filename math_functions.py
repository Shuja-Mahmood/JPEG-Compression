import math

#Quantization Matrix
Q = [[16, 11, 10, 16,  24,  40,  51,  61],
     [12, 12, 14, 19,  26,  58,  60,  55],
     [14, 13, 16, 24,  40,  57,  69,  56],
     [14, 17, 22, 29,  51,  87,  80,  62],
     [18, 22, 37, 56,  68, 109, 103,  77],
     [24, 35, 55, 64,  81, 104, 113,  92],
     [49, 64, 78, 87, 103, 121, 120, 101],
     [72, 92, 95, 98, 112, 100, 103,  99]]


def image_to_intensity(image, offset = -128):
    """returns 2D array of color intensity of image"""

    intensity = []
    
    for j in range(image.size[1]):
        # Iterate through each row
        row = []
        
        for i in range(image.size[0]):
            # Iterate through each element in row
            row.append(image.getpixel((i, j)) + offset)
        
        intensity.append(row)
    
    return intensity


def round_to_integer(matrix, offset = 128):
    """returns 2D array with each element rounded to intergers"""
    
    intensity = []
    
    for i in range(len(matrix)):
        # Iterate through each row
        row = []
        
        for j in range(len(matrix[0])):
            # Iterate through each element in row
            row.append(round(matrix[i][j]) + offset)
        
        intensity.append(row)
    
    return intensity


def alpha(n):
    """Normalizing scale factor"""

    return 1 / math.sqrt(2) if n == 0 else 1


def dct_2d(matrix):
    """returns the 2D discrete cosine transform of an 8x8 matrix"""
    
    dct = []
    
    for v in range(8):
        # Iterate throught each row
        row = []
        
        for u in range(8):
            # Iterate throught each element in row
            n = 0
            
            for x in range(8):
                
                for y in range(8):
                    # Compute DCT of one element
                    n += matrix[y][x] * math.cos((2*x + 1)*u*math.pi/16) * math.cos((2*y + 1)*v*math.pi/16)
            
            n *= (alpha(u) * alpha(v))/4    
            row.append(n)
        
        dct.append(row)
    
    return dct


def inverse_dct_2d(matrix):
    """returns the inverse 2D discrete cosine transform of an 8x8 matrix"""
    
    i_dct = []
    
    for y in range(8):
        # Iterate throught each row
        row = []
        
        for x in range(8):
            # Iterate throught each element in row
            n = 0
            # Compute inverse DCT of one element
            for u in range(8):
                
                for v in range(8):
                    n += alpha(u) * alpha(v) * matrix[u][v] * math.cos((2*x + 1)*u*math.pi/16) * math.cos((2*y + 1)*v*math.pi/16)
            
            n /= 4        
            row.append(n)
        
        i_dct.append(row)
    
    return i_dct


def quantization(matrix, quantization_matrix = Q):
    """Quantizes a matrix using Quantization matrix"""
    
    quantized = []
    
    for j in range(len(matrix)):
        # Iterate throught each row
        row = []
        
        for i in range(len(matrix[j])):
            # Divide matrix element with corresponding quantization element
            row.append(round(matrix[j][i] / quantization_matrix[j][i]))
        
        quantized.append(row)
    
    return quantized


def dequantization(matrix, quantization_matrix = Q):
    """Dequantizes a matrix using Quantization matrix"""
    
    dequantized = []
    
    for j in range(len(matrix)):
        # Iterate throught each row
        row = []
        
        for i in range(len(matrix[j])):
            # Multiply matrix element with corresponding quantization element
            row.append(matrix[j][i] * quantization_matrix[j][i])
        
        dequantized.append(row)
    
    return dequantized


def entropy_encoding(matrix):
    """converts a matrix into 1D array in 'entropy' order"""
    
    n = len(matrix)

    if n != len(matrix[0]):
        print("Matrix is not square")
        return

    # 1D array container
    array = []
    for i in range(n):
        # Iterate through upper left triangle (including centeral diagonal)
        for j in range(i+1):
            # Each nth diagonal contains n+1 elements
            if j == 0:
                # Initialize indexes
                x = i
                y = 0
            if i % 2 == 0:
                # Moving up the diagonal
                array.append(matrix[x][y])
            else:
                # Moving down the diagonal
                array.append(matrix[y][x])
            # Move to next element
            x -= 1
            y += 1
    for i in range(n - 1, 0, -1):
        # Iterate lower right triangle (excluding central diagonal)
        for j in range(i):
            # Each nth diagonal contains n elements
            if j == 0:
                # Initialize indexes
                x = n - i
                y = n - 1
            if i % 2 == 0:
                # Move up the diagonal
                array.append(matrix[x][y])
            else:
                # Move down th diagonal
                array.append(matrix[y][x])
            # Move to next element
            x += 1
            y -= 1
    return array


def entropy_decoding(array, n = 8):
    """converts a 1D 'entropy' encoded array to n x n matrix"""

    count = 0
    # 2D array container
    matrix = [[0 for i in range(n)] for i in range(n)]

    for i in range(n):
        # Iterate through upper left triangle (including centeral diagonal)
        for j in range(i+1):
            # Each nth diagonal contains n+1 elements
            if j == 0:
                # Initialize indexes
                x = i
                y = 0
            if i % 2 == 0:
                # Moving up the diagonal
                matrix[x][y] = array[count]
            else:
                # Moving down the diagonal
                matrix[y][x] = array[count]
            # Move to next element
            x -= 1
            y += 1
            count += 1
    for i in range(n - 1, 0, -1):
        # Iterate lower triangle (excluding central diagonal)
        for j in range(i):
            # Each nth diagonal contains n elements
            if j == 0:
                # Initialize indexes
                x = n - i
                y = n - 1
            if i % 2 == 0:
                # Move up the diagonal
                matrix[x][y] = array[count]
            else:
                # Move down th diagonal
                matrix[y][x] = array[count]
            # Move to next element
            x += 1
            y -= 1
            count += 1
    return matrix


def decrease_quality(array, n = 64):
    """reduces size of array to n elements by setting last elements to 0"""

    # convert n to integer
    n = int(n)
    
    if len(array) < n:
        print("Array length lower than quality, returning original array")
        return array
    
    for i in range(len(array) - n):
        # set value to zero starting from the last element
        array[-i - 1] = 0
    
    return array
