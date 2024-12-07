import json
import argparse
from typing import Dict, List, Any

class IIIFConverter:
    def __init__(self, context_url: str, base_image_url: str, motivation: str):
        self.context_url = context_url
        self.base_image_url = base_image_url
        self.motivation = motivation

    def convert_coordinates(self, box: List[int]) -> str:
        """Convert box coordinates to IIIF format (x,y,w,h)"""
        x = box[0]
        y = box[1]
        w = box[2] - box[0]
        h = box[3] - box[1]
        return f"xywh={x},{y},{w},{h}"

    def create_annotation(self, content: str, box: List[int], order: int) -> Dict[str, Any]:
        """Create a single IIIF annotation"""
        return {
            "@context": self.context_url,
            "type": "Annotation",
            "motivation": self.motivation,
            "body": {
                "type": "TextualBody",
                "value": content,
                "format": "text/plain",
                "language": "ja"
            },
            "target": {
                "source": self.base_image_url,
                "selector": {
                    "type": "FragmentSelector",
                    "value": self.convert_coordinates(box)
                }
            },
            "order": order
        }

    def convert_file(self, input_json: Dict[str, Any]) -> Dict[str, Any]:
        """Convert entire JSON file to IIIF format"""
        annotations = []
        
        # Convert paragraphs
        for para in input_json.get("paragraphs", []):
            if "contents" in para and "box" in para:
                annotation = self.create_annotation(
                    para["contents"],
                    para["box"],
                    para.get("order", 0)
                )
                annotations.append(annotation)

        return {
            "@context": self.context_url,
            "type": "AnnotationPage",
            "items": annotations
        }

def main():
    parser = argparse.ArgumentParser(description='Convert JSON to IIIF Annotation format')
    parser.add_argument('input_file', help='Input JSON file path')
    parser.add_argument('output_file', help='Output IIIF JSON file path')
    parser.add_argument('--context', default="http://iiif.io/api/presentation/3/context.json",
                      help='IIIF context URL')
    parser.add_argument('--image', required=True,
                      help='Base image URL')
    parser.add_argument('--motivation', default="transcribing",
                      help='Annotation motivation (e.g., transcribing, commenting)')

    args = parser.parse_args()

    # Read input JSON
    with open(args.input_file, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

    # Convert to IIIF
    converter = IIIFConverter(args.context, args.image, args.motivation)
    iiif_data = converter.convert_file(input_data)

    # Write output
    with open(args.output_file, 'w', encoding='utf-8') as f:
        json.dump(iiif_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
