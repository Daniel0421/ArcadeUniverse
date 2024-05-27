import subprocess
import os

def remove_icc_profile(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".png"):
                file_path = os.path.join(root, file)
                subprocess.run(["pngcrush", "-ow", "-rem", "allb", "-reduce", file_path])
