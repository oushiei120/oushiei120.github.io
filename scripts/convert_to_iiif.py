import json
import os

def convert_to_iiif(input_json_path, image_url):
    # 读取输入的JSON文件
    with open(input_json_path, 'r', encoding='utf-8') as f:
        source_data = json.load(f)
    
    # 创建IIIF注释列表
    annotations = []
    
    # 处理段落
    for para in source_data.get("paragraphs", []):
        if "contents" in para and "box" in para:
            # 转换坐标为IIIF格式 (x,y,w,h)
            box = para["box"]
            x = box[0]
            y = box[1]
            w = box[2] - box[0]
            h = box[3] - box[1]
            
            # 创建单个注释
            annotation = {
                "@context": "http://iiif.io/api/presentation/3/context.json",
                "type": "Annotation",
                "motivation": "transcribing",
                "body": {
                    "type": "TextualBody",
                    "value": para["contents"],
                    "format": "text/plain",
                    "language": "ja"
                },
                "target": {
                    "source": image_url,
                    "selector": {
                        "type": "FragmentSelector",
                        "value": f"xywh={x},{y},{w},{h}"
                    }
                },
                "order": para.get("order", 0)
            }
            annotations.append(annotation)
    
    # 创建IIIF AnnotationPage
    iiif_data = {
        "@context": "http://iiif.io/api/presentation/3/context.json",
        "type": "AnnotationPage",
        "items": annotations
    }
    
    # 生成输出文件名
    input_dir = os.path.dirname(input_json_path)
    input_filename = os.path.basename(input_json_path)
    output_filename = f"iiif_{input_filename}"
    output_path = os.path.join(input_dir, output_filename)
    
    # 保存IIIF JSON文件
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(iiif_data, f, ensure_ascii=False, indent=2)
    
    return output_path

# 使用示例
if __name__ == "__main__":
    # 设置输入文件路径和图像URL
    input_path = "/Users/oushiei/Documents/GitHub/oushiei120.github.io/json/page1_page1_p1.json"  # 修改为你的输入文件路径
    image_url = "https://example.org/images/page1.jpg"  # 修改为你的图像URL
    
    # 执行转换
    output_path = convert_to_iiif(input_path, image_url)
    print(f"转换完成！IIIF文件已保存到: {output_path}")
