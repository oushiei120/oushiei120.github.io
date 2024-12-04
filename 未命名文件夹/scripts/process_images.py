import os
import subprocess
import json
from urllib.parse import quote

def create_iiif_image(input_path, output_dir):
    """Convert an image to IIIF format using vips"""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get the filename without extension and encode for URL
    filename = os.path.splitext(os.path.basename(input_path))[0]
    safe_filename = quote(filename)
    
    # Get image dimensions using vips
    header_info = subprocess.check_output(['vipsheader', '-a', input_path]).decode()
    width = height = 0
    for line in header_info.split('\n'):
        if 'width:' in line:
            width = int(line.split(':')[1].strip())
        elif 'height:' in line:
            height = int(line.split(':')[1].strip())
    
    if width == 0 or height == 0:
        raise ValueError(f"Could not determine dimensions for {input_path}")
    
    # Create the IIIF directory for this image
    image_dir = os.path.join(output_dir, safe_filename)
    os.makedirs(image_dir, exist_ok=True)
    
    # Convert the image using vips
    subprocess.run([
        'vips',
        'dzsave',
        input_path,
        image_dir,
        '--layout', 'iiif',
        '--tile-size', '256',
        '--overlap', '0',
        '--depth', 'onepixel'
    ])
    
    return safe_filename, width, height

def create_simple_manifest(image_info_list, output_path):
    """Create a basic IIIF manifest for the images"""
    manifest = {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@type": "sc:Manifest",
        "@id": "https://oushiei120.github.io/iiif/manifests/manifest.json",
        "label": "Japanese Document Pages",
        "sequences": [
            {
                "@type": "sc:Sequence",
                "canvases": []
            }
        ]
    }
    
    for idx, (image_name, width, height) in enumerate(image_info_list):
        # Create canvas
        canvas = {
            "@type": "sc:Canvas",
            "@id": f"https://oushiei120.github.io/iiif/canvas/p{idx+1}",
            "label": f"p. {idx+1}",
            "height": height,
            "width": width,
            "images": [
                {
                    "@type": "oa:Annotation",
                    "motivation": "sc:painting",
                    "@id": f"https://oushiei120.github.io/iiif/annotation/p{idx+1}",
                    "resource": {
                        "@id": f"https://oushiei120.github.io/iiif/processed_images/{image_name}/full/full/0/default.jpg",
                        "@type": "dctypes:Image",
                        "height": height,
                        "width": width,
                        "service": {
                            "@context": "http://iiif.io/api/image/2/context.json",
                            "@id": f"https://oushiei120.github.io/iiif/processed_images/{image_name}",
                            "profile": "http://iiif.io/api/image/2/level2.json"
                        }
                    },
                    "on": f"https://oushiei120.github.io/iiif/canvas/p{idx+1}"
                }
            ]
        }
        
        manifest["sequences"][0]["canvases"].append(canvas)
    
    # Write the manifest
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

def main():
    # Define paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    images_dir = os.path.join(base_dir, 'images')
    iiif_dir = os.path.join(base_dir, 'iiif', 'processed_images')
    manifest_dir = os.path.join(base_dir, 'iiif', 'manifests')
    
    # Create output directories
    os.makedirs(iiif_dir, exist_ok=True)
    os.makedirs(manifest_dir, exist_ok=True)
    
    # Get image files (specifically the three Chinese-named files)
    target_files = ['第 1 页.png', '第 2 页.png', '第 3 页.png']
    image_files = [f for f in target_files if f in os.listdir(images_dir)]
    
    # Process images
    image_info_list = []
    for image_file in image_files:
        input_path = os.path.join(images_dir, image_file)
        image_name, width, height = create_iiif_image(input_path, iiif_dir)
        image_info_list.append((image_name, width, height))
    
    # Create manifest
    manifest_path = os.path.join(manifest_dir, 'manifest.json')
    create_simple_manifest(image_info_list, manifest_path)

if __name__ == '__main__':
    main()
