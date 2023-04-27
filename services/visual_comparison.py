from PIL import Image
import os


def compare_images(img1, img2, image_folder, result_folder, threshold):
    img1 = Image.open(os.path.join(image_folder, img1)).convert('RGB')
    img2 = Image.open(os.path.join(image_folder, img2)).convert('RGB')
    diff = Image.new('RGB', img1.size, (255, 255, 255))

    for x in range(img1.width):
        for y in range(img1.height):
            r1, g1, b1 = img1.getpixel((x, y))
            r2, g2, b2 = img2.getpixel((x, y))
            if abs(r1 - r2) > threshold or abs(g1 - g2) > threshold or abs(b1 - b2) > threshold:
                diff.putpixel((x, y), (255, 0, 0))

    result_file = os.path.join(result_folder, 'result.png')
    diff.save(result_file)
    return result_file


def get_diff_percent(img1, img2, image_folder, threshold):
    img1 = Image.open(os.path.join(image_folder, img1)).convert('RGB')
    img2 = Image.open(os.path.join(image_folder, img2)).convert('RGB')

    num_pixels = img1.width * img1.height
    num_diff_pixels = 0

    for x in range(img1.width):
        for y in range(img1.height):
            r1, g1, b1 = img1.getpixel((x, y))
            r2, g2, b2 = img2.getpixel((x, y))
            if abs(r1 - r2) > threshold or abs(g1 - g2) > threshold or abs(b1 - b2) > threshold:
                num_diff_pixels += 1

    diff_percent = num_diff_pixels / num_pixels * 100
    return diff_percent
