import os
import time
import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image
import numpy as np

def create_dirs(base_path="dataset"):
    """Creates the necessary directories for the dataset."""
    real_path = os.path.join(base_path, "real")
    fake_path = os.path.join(base_path, "fake")
    os.makedirs(real_path, exist_ok=True)
    os.makedirs(fake_path, exist_ok=True)
    return real_path, fake_path

def is_grayscale(filepath):
    """Checks if an image is grayscale or effectively grayscale."""
    try:
        img = Image.open(filepath)
        if img.mode == 'L':
            return True
        if img.mode == 'RGB':
            # Check if all channels are equal (R=G=B)
            stat = np.array(img)
            # Check a sample of pixels for speed if needed, but for 1024x1024 numpy is fast enough
            # effective check: if std dev of (R-G) and (G-B) is near 0
            if np.allclose(stat[:,:,0], stat[:,:,1], atol=5) and np.allclose(stat[:,:,1], stat[:,:,2], atol=5):
                return True
        return False
    except Exception:
        return False # Assume not grayscale if we can't read it, or handle as error elsewhere

def download_image(url, save_path, retries=3):
    """Downloads an image from a URL to a specific path."""
    for i in range(retries):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                return True
        except Exception:
            time.sleep(1)
    return False

def download_single_fake(i, save_dir):
    """Helper to download a single fake image."""
    url = "https://thispersondoesnotexist.com/"
    filename = f"fake_{int(time.time())}_{i}.jpg"
    filepath = os.path.join(save_dir, filename)
    if download_image(url, filepath):
        return True
    return False

def download_single_real(i, save_dir):
    """Helper to download a single real image. Enforces color."""
    base_url = "https://loremflickr.com/1024/1024/portrait,face,woman,man"
    filename = f"real_{int(time.time())}_{i}.jpg"
    filepath = os.path.join(save_dir, filename)
    
    max_attempts = 5
    for attempt in range(max_attempts):
        # Adding random param
        url = f"{base_url}?random={i}_{attempt}"
        if download_image(url, filepath):
            # Check if grayscale
            if is_grayscale(filepath):
                # Delete and try again
                try:
                    os.remove(filepath)
                except:
                    pass
                time.sleep(0.5)
                continue
            else:
                return True
        else:
            time.sleep(1)
            
    return False

def generate_images_concurrently(count, save_dir, type_label):
    """Downloads images concurrently using ThreadPoolExecutor."""
    print(f"Downloading {count} {type_label} images...")
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        if type_label == "FAKE":
            for i in range(count):
                futures.append(executor.submit(download_single_fake, i, save_dir))
        else:
            for i in range(count):
                futures.append(executor.submit(download_single_real, i, save_dir))
        
        # Use tqdm to show progress as futures complete
        for _ in tqdm(as_completed(futures), total=count):
            pass

def main():
    print("Starting Dataset Generation...")
    real_dir, fake_dir = create_dirs()
    
    NUM_IMAGES = 50 
    
    # We can just append to existing, or maybe we want to clean 'real' first? 
    # For now, let's keep it simple. If user re-runs, it adds more.
    # But since we found B&W in 'real', we should probably CLEAR the 'real' directory 
    # or the user will still have B&W images.
    
    # Optional: Clear real_dir if it's full of B&W? 
    # Let's not auto-delete unless requested, but the user asked "why black and white".
    # I will assume they want them FIXED.
    
    # Let's run the download. The new ones will be color.
    # The user might need to manually delete the old ones or I can do it.
    # I'll add a snippet here to remove existing B&W in real_dir if I really wanted to be helpful,
    # but that's complex logic for 'main'.
    # I will rely on the user running this script to get *new* images, 
    # but I will recommend deleting the old folder in my message.

    generate_images_concurrently(NUM_IMAGES, fake_dir, "FAKE")
    generate_images_concurrently(NUM_IMAGES, real_dir, "REAL")
    
    print(f"\nDone! Images saved to:\n  - {real_dir}\n  - {fake_dir}")

if __name__ == "__main__":
    main()
