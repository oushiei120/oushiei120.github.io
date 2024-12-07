import json
import os

def convert_to_iiif(input_json_path, base_url, image_height):
    # 读取输入的JSON文件
    with open(input_json_path, 'r', encoding='utf-8') as f:
        source_data = json.load(f)
    
    # 创建IIIF注释列表
    annotations = []
    
    # 处理段落
    for idx, para in enumerate(source_data.get("paragraphs", [])):
        if "contents" in para and "box" in para:
            # 转换坐标为IIIF格式 (x,y,w,h)
            box = para["box"]
            x = box[0]
            # 转换y坐标（因为IIIF使用从上到下的坐标系统）
            y = image_height - box[3]
            w = box[2] - box[0]
            h = box[3] - box[1]
            
            # 创建单个注释
            annotation = {
                "id": f"{base_url}/iiif/annotation/p1-text-{idx+1}",
                "@context": "http://iiif.io/api/presentation/3/context.json",
                "type": "Annotation",
                "motivation": "supplementing",
                "body": {
                    "type": "TextualBody",
                    "value": para["contents"],
                    "format": "text/plain",
                    "language": "ja"
                },
                "target": {
                    "source": f"{base_url}/iiif/canvas/p1",
                    "selector": {
                        "type": "FragmentSelector",
                        "value": f"xywh={x},{y},{w},{h}"
                    }
                }
            }
            annotations.append(annotation)
    
    # 创建IIIF AnnotationPage
    iiif_data = {
        "@context": "http://iiif.io/api/presentation/3/context.json",
        "id": f"{base_url}/iiif/annotation1.json",
        "type": "AnnotationPage",
        "items": annotations
    }
    
    # 生成输出文件路径
    output_path = "/Users/oushiei/Documents/GitHub/oushiei120.github.io/iiif/annotation1.json"
    
    # 保存IIIF JSON文件
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(iiif_data, f, ensure_ascii=False, indent=2)
    
    return output_path

# 使用示例
if __name__ == "__main__":
    # 设置输入文件路径和基础URL
    input_path = "/Users/oushiei/Documents/GitHub/oushiei120.github.io/json/page1_page1_p1.json"
    base_url = "https://oushiei120.github.io"
    image_height = 1850  # 图像高度
    
    # 执行转换
    output_path = convert_to_iiif(input_path, base_url, image_height)
    print(f"转换完成！IIIF文件已保存到: {output_path}")
