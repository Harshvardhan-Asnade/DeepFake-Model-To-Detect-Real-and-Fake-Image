"""
Script to download modern AI-generated faces for improving the deepfake detection model
"""

import requests
import os
import time
from PIL import Image
from io import BytesIO

def download_thispersondoesnotexist(num_images=1000, output_dir='dataset/fake '):
    """
    Download AI-generated faces from ThisPersonDoesNotExist.com
    
    Args:
        num_images: Number of images to download
        output_dir: Directory to save images
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Get current max number in fake folder
    existing_files = [f for f in os.listdir(output_dir) if f.endswith('.jpg')]
    if existing_files:
        numbers = [int(f.split('.')[0]) for f in existing_files if f.split('.')[0].isdigit()]
        start_num = max(numbers) + 1 if numbers else 0
    else:
        start_num = 0
    
    print(f"📥 Downloading {num_images} AI-generated faces from ThisPersonDoesNotExist.com")
    print(f"Starting from image number: {start_num}")
    print("=" * 60)
    
    successful = 0
    failed = 0
    
    for i in range(num_images):
        image_num = start_num + i
        filename = f"{image_num}.jpg"
        filepath = os.path.join(output_dir, filename)
        
        try:
            # Download image (they use a random cache-busting parameter)
            url = f"https://thispersondoesnotexist.com/?{time.time()}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                # Save image
                img = Image.open(BytesIO(response.content))
                img.save(filepath, 'JPEG')
                successful += 1
                
                if (i + 1) % 10 == 0:
                    print(f"✓ Downloaded {i + 1}/{num_images} images... (Success: {successful}, Failed: {failed})")
            else:
                failed += 1
                print(f"✗ Failed to download image {i + 1}: HTTP {response.status_code}")
            
            # Respectful delay to avoid overwhelming the server
            time.sleep(1.5)
            
        except Exception as e:
            failed += 1
            print(f"✗ Error downloading image {i + 1}: {str(e)}")
            time.sleep(2)  # Longer delay after error
    
    print("\n" + "=" * 60)
    print(f"✅ Download complete!")
    print(f"   Successful: {successful}")
    print(f"   Failed: {failed}")
    print(f"   Saved to: {output_dir}")
    print("=" * 60)

def check_dataset_distribution(dataset_dir='dataset'):
    """Check current distribution of real vs fake images"""
    fake_dir = os.path.join(dataset_dir, 'fake ')
    real_dir = os.path.join(dataset_dir, 'real')
    
    fake_count = len([f for f in os.listdir(fake_dir) if f.endswith(('.jpg', '.png', '.jpeg'))])
    real_count = len([f for f in os.listdir(real_dir) if f.endswith(('.jpg', '.png', '.jpeg'))])
    
    print("\n📊 Current Dataset Distribution:")
    print("=" * 60)
    print(f"Fake images: {fake_count:,}")
    print(f"Real images: {real_count:,}")
    print(f"Total images: {fake_count + real_count:,}")
    print(f"Balance ratio: {fake_count/real_count:.2f} (ideal: ~1.0)")
    print("=" * 60 + "\n")
    
    return fake_count, real_count

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Download modern AI-generated faces')
    parser.add_argument('--num', type=int, default=1000, 
                        help='Number of images to download (default: 1000)')
    parser.add_argument('--output', type=str, default='dataset/fake ',
                        help='Output directory (default: dataset/fake )')
    
    args = parser.parse_args()
    
    # Check current dataset
    print("\n🔍 Checking current dataset...")
    check_dataset_distribution()
    
    # Confirm download
    print(f"\n⚠️  About to download {args.num} AI-generated images")
    print(f"   This will take approximately {args.num * 1.5 / 60:.1f} minutes")
    response = input("   Continue? (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        download_thispersondoesnotexist(args.num, args.output)
        
        # Show updated distribution
        print("\n🔍 Updated dataset distribution:")
        check_dataset_distribution()
        
        print("\n✨ Next steps:")
        print("1. Run: python model/main.py --dataset ./dataset --epochs 30")
        print("2. Test the improved model with your deepfake images")
        print("3. Check the confusion matrix for balanced performance")
    else:
        print("❌ Download cancelled")
