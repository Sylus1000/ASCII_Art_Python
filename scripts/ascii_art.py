import os
import argparse
import numpy as np
import time
from PIL import Image, ImageFont, ImageSequence

ASCII_CHARS = [' ', '.', ':', '-', '=', '+', '*', '#', '%', '@', '0', '9']

def get_ascii_char(pixel_value):
    if pixel_value < 0 or pixel_value > 255:
        print('Invalid pixel value:', pixel_value)
    # map the pixel value to an index in the ASCII_CHARS list
    index = int(pixel_value / 25.5)
    return ASCII_CHARS[index]

def process_image_auto(image_path, output_name, scale=1, font_size=12):
    if output_name is not None:
        dest_dir = f"./results/{time.time()}"
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, output_name)
    if isinstance(image_path, str):
        image = Image.open(image_path).convert('L')
    else:
        image = image_path.convert('L')
    # calculate the number of columns and rows to use for the ASCII image
    aspect_ratio = image.size[0] / image.size[1]
    cols = int(120 * aspect_ratio)
    rows = int(cols / aspect_ratio / 2)
    # calculate the size of each character in the ASCII image
    font = ImageFont.truetype('cour.ttf', font_size)
    char_bbox = font.getbbox('A')
    char_width, char_height = char_bbox[2] - char_bbox[0], char_bbox[3] - char_bbox[1]
    # resize the image and convert the pixel data to ASCII characters
    width, height = int(cols * char_width * scale), int(rows * char_height * scale)
    image = image.resize((width, height))
    pixels = np.array(list(image.getdata()))
    pixels = pixels.reshape((height, width))
    ascii_chars = [[get_ascii_char(pixel) for pixel in row] for row in pixels]
    ascii_image = '\n'.join([''.join(row) for row in ascii_chars])
    # save the ASCII art to a text file
    if output_name is not None:
        with open(dest_path, 'w') as f:
            f.write(ascii_image)
    return ascii_image

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--img', '-i', type=str, default='fors.jpg', help='image to convert to ASCII-Art')
    parser.add_argument('--scale', '-s', type=float, default=0.1, help='new size of the resulting ASCII-Image relative to original img dims')
    parser.add_argument('--font-size', '-f', type=int, default=12, help='font size')
    parser.add_argument('--output', '-o', type=str, default='ascii_art', help='output filename (not path)')
    opt = parser.parse_args()

    image_path = opt.img
    output_name = opt.output
    scale = opt.scale
    font_size = opt.font_size

    if image_path.endswith('.gif'):
        im = Image.open(image_path)
        num_frames = im.n_frames
        fps = 30 if num_frames // 60 <= 1 else 60
        print(f"Number of frames: {num_frames}, FPS: {fps}")
        time.sleep(2)
        ascii_frames = []
        for frame in ImageSequence.Iterator(im):
            ascii_image = process_image_auto(frame, None, scale, font_size)
            ascii_frames.append(ascii_image)

        current_index = 0
        while(True):
            os.system('cls' if os.name == 'nt' else 'clear') # clear the console
            if current_index < len(ascii_frames):
                print(ascii_frames[current_index])
                current_index+=1
            else:
                current_index=0
                print(ascii_frames[current_index])
            time.sleep(1 / fps)
    else:
        process_image_auto(image_path, output_name, scale, font_size)

