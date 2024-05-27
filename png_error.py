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

def getGameList():
    gamelist = []
    currentDirectory = os.getcwd()
    for entry in os.listdir(currentDirectory):
        if os.path.isdir(os.path.join(currentDirectory, entry)) and entry[0].isupper() and not entry.startswith(
                "P"):
            gamelist.append(entry)
    return sorted(gamelist)
gameList = getGameList()

for game in gameList:
    gameDir = os.path.join(os.getcwd(), game)
    pngDir = os.path.join(gameDir, 'assets', 'gif')
    if os.path.isdir(pngDir):
        remove_icc_profile(pngDir)
