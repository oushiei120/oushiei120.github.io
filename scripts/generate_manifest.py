import os
import json
from PIL import Image
from urllib.parse import quote

def get_image_dimensions(image_path):
    """获取图像尺寸"""
    with Image.open(image_path) as img:
        return img.size

def load_text_annotations(json_dir, image_filename):
    """加载对应图像的文本注释"""
    base_name = os.path.splitext(image_filename)[0]
    json_path = os.path.join(json_dir, f"{base_name}.json")
    
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('paragraphs', [])
    return []

def generate_manifest(images_dir, json_dir):
    """生成IIIF manifest"""
    manifest = {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@type": "sc:Manifest",
        "@id": "https://oushiei120.github.io/iiif/manifests/manifest.json",
        "label": "Image Collection with Annotations",
        "sequences": [
            {
                "@type": "sc:Sequence",
                "canvases": []
            }
        ]
    }

    # 获取所有图像文件
    image_files = [f for f in os.listdir(images_dir) if f.endswith(('.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG'))]
    image_files.sort()  # 按文件名排序

    for index, image_file in enumerate(image_files, 1):
        # 获取图像尺寸
        image_path = os.path.join(images_dir, image_file)
        width, height = get_image_dimensions(image_path)
        
        # 获取文本注释
        annotations = load_text_annotations(json_dir, image_file)
        
        # URL编码图像文件名
        encoded_filename = quote(image_file)
        
        # 创建画布
        canvas = {
            "@type": "sc:Canvas",
            "@id": f"https://oushiei120.github.io/iiif/canvas/p{index}",
            "label": f"p. {index}",
            "height": height,
            "width": width,
            "images": [
                {
                    "@type": "oa:Annotation",
                    "motivation": "sc:painting",
                    "@id": f"https://oushiei120.github.io/iiif/annotation/p{index}",
                    "resource": {
                        "@id": f"https://oushiei120.github.io/images/{encoded_filename}",
                        "@type": "dctypes:Image",
                        "format": "image/png" if image_file.lower().endswith('.png') else "image/jpeg",
                        "height": height,
                        "width": width
                    },
                    "on": f"https://oushiei120.github.io/iiif/canvas/p{index}"
                }
            ],
            "otherContent": [
                {
                    "@type": "sc:AnnotationList",
                    "@id": f"https://oushiei120.github.io/iiif/annotations/p{index}.json",
                    "resources": [
                        {
                            "@type": "oa:Annotation",
                            "motivation": "sc:commenting",
                            "@id": f"https://oushiei120.github.io/iiif/annotation/comment-{index}-{i}",
                            "resource": {
                                "@type": "dctypes:Text",
                                "format": "text/plain",
                                "chars": anno["contents"],
                                "metadata": {
                                    "box": anno["box"],
                                    "direction": anno["direction"],
                                    "role": anno["role"]
                                }
                            },
                            "on": f"https://oushiei120.github.io/iiif/canvas/p{index}#xywh={','.join(map(str, anno['box']))}"
                        }
                        for i, anno in enumerate(annotations)
                    ]
                }
            ] if annotations else []
        }
        
        manifest["sequences"][0]["canvases"].append(canvas)
    
    return manifest

def main():
    # 设置路径
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    images_dir = os.path.join(base_dir, 'images')
    json_dir = os.path.join(base_dir, 'json')
    manifest_dir = os.path.join(base_dir, 'iiif', 'manifests')
    
    # 确保manifest目录存在
    os.makedirs(manifest_dir, exist_ok=True)
    
    # 生成manifest
    manifest = generate_manifest(images_dir, json_dir)
    
    # 保存manifest文件
    manifest_path = os.path.join(manifest_dir, 'manifest.json')
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    
    print(f"Manifest已生成: {manifest_path}")

if __name__ == "__main__":
    main()
