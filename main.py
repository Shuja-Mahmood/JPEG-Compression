# Compress grey scale images using JPEG compression
# This method will use Discrete Cosine Transform
# Additional info: https://en.wikipedia.org/wiki/JPEG


import math_functions
import image_functions

IMAGE_LOCATION = "test image.tiff"

QUALITY = 64    # integer between (and including) 0 and 64

image = image_functions.Image.open(IMAGE_LOCATION)


def main():

    # 2D matrix of image blocks
    blocks = image_functions.split_image(image)

    # Compressed and Decompressed blocks
    new_blocks = []

    for j in blocks:
        # Iterate through each row of image blocks
        row = []
        for i in j:
            # Iterate through each block in row

            # Convert image to DCT matrix
            uncompressed = math_functions.entropy_encoding(math_functions.quantization(math_functions.dct_2d(math_functions.image_to_intensity(i))))
            
            # Remove high frequencies
            compressed = math_functions.decrease_quality(uncompressed, QUALITY)
            
            # Recover image from compressed data
            row.append(image_functions.matrix_to_pixels(math_functions.round_to_integer(math_functions.inverse_dct_2d(math_functions.dequantization(math_functions.entropy_decoding(compressed))))))

        new_blocks.append(row)
    final_image = image_functions.stitch_images(new_blocks)
    final_image.save("Compressed_%s.jpeg" % (QUALITY))
    final_image.show()


if __name__ == "__main__":
    main()
