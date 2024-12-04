import json
import os
import uuid

def create_annotation(word, canvas_id):
    """Create a IIIF annotation from OCR word data"""
    if 'box' in word:
        [x1, y1, x2, y2] = word['box']
    else:
        points = word['points']
        x1, y1 = points[0]
        x2, y2 = points[2]  # 使用对角点
    
    width = x2 - x1
    height = y2 - y1
    
    return {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@type": "oa:Annotation",
        "@id": f"https://oushiei120.github.io/iiif/annotations/{uuid.uuid4()}",
        "motivation": "sc:supplementing",
        "resource": {
            "@type": "dctypes:Text",
            "chars": word['content'],
            "format": "text/plain",
            "language": "ja",
            "metadata": [
                {
                    "label": "Direction",
                    "value": word['direction']
                },
                {
                    "label": "Confidence",
                    "value": str(word['det_score'])
                }
            ]
        },
        "on": {
            "@type": "oa:SpecificResource",
            "full": canvas_id,
            "selector": {
                "@type": "oa:FragmentSelector",
                "value": f"xywh={x1},{y1},{width},{height}"
            }
        }
    }

def create_annotation_list(annotations, page_number):
    """Create a IIIF annotation list"""
    return {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@type": "sc:AnnotationList",
        "@id": f"https://oushiei120.github.io/iiif/annotations/page{page_number}/list.json",
        "resources": annotations
    }

def convert_ocr_to_annotations():
    # 确保输出目录存在
    os.makedirs("../iiif/annotations", exist_ok=True)
    
    # 读取manifest获取canvas信息
    with open("../iiif/manifests/manifest.json", "r", encoding="utf-8") as f:
        manifest = json.load(f)
    
    canvases = manifest['sequences'][0]['canvases']
    
    # 处理每个页面的OCR结果
    for i, canvas in enumerate(canvases, 1):
        canvas_id = canvas['@id']
        
        # 读取OCR结果
        try:
            with open(f"../json/page{i}.json", "r", encoding="utf-8") as f:
                ocr_data = json.load(f)
        except FileNotFoundError:
            print(f"Warning: No OCR data found for page {i}")
            continue
        
        # 转换每个词为annotation
        annotations = [create_annotation(word, canvas_id) for word in ocr_data['words']]
        
        # 创建annotation list
        annotation_list = create_annotation_list(annotations, i)
        
        # 保存annotation list
        os.makedirs(f"../iiif/annotations/page{i}", exist_ok=True)
        with open(f"../iiif/annotations/page{i}/list.json", "w", encoding="utf-8") as f:
            json.dump(annotation_list, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    convert_ocr_to_annotations()
