import os
from PIL import Image
import numpy as np

def check_colors(directory):
    print(f"Checking images in {directory}...")
    grayscale_count = 0
    color_count = 0
    total = 0
    
    if not os.path.exists(directory):
        print("Directory not found.")
        return

    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            total += 1
            path = os.path.join(directory, filename)
            try:
                img = Image.open(path)
                # Check mode
                if img.mode == 'L':
                    grayscale_count += 1
                elif img.mode == 'RGB':
                    # Sometimes RGB images are actually just gray pixels
                    stat = np.array(img)
                    if np.all(stat[:,:,0] == stat[:,:,1]) and np.all(stat[:,:,1] == stat[:,:,2]):
                        grayscale_count += 1
                    else:
                        color_count += 1
                else:
                    # RGBA etc
                    color_count += 1
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    
    print(f"Total: {total}")
    print(f"Grayscale (B&W): {grayscale_count}")
    print(f"Color: {color_count}")

print("--- Real Images ---")
check_colors("dataset/real")
print("\n--- Fake Images ---")
check_colors("dataset/fake")
