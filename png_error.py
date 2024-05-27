from PIL import Image
import os

def remove_icc_profile(image_folder):
    for root, _, files in os.walk(image_folder):
        for file in files:
            if file.endswith('.png'):
                image_path = os.path.join(root, file)
                with Image.open(image_path) as img:
                    if 'icc_profile' in img.info:
                        print(f'Removing ICC profile from {image_path}')
                        data = list(img.getdata())
                        img_without_icc = Image.new(img.mode, img.size)
                        img_without_icc.putdata(data)
                        img_without_icc.save(image_path)

# Example usage
currDir = os.getcwd()
folderPath = os.path.join(currDir, 'Mine Sweeper', 'assets', 'gif')
remove_icc_profile(folderPath)
