from transformers import AutoImageProcessor, AutoModelForObjectDetection
import torch
from PIL import Image

# url = "http://images.cocodataset.org/val2017/000000039769.jpg"
# image = Image.open(requests.get(url, stream=True).raw)

# image = Image.open('image_subset/manual-review/sa_223750.jpg')

class YoloDetector():
    '''
    Takes in a PIL image, returns bounding boxes detected by a YOLOS model.
    '''
    def __init__(self, yolos_model="hustvl/yolos-base"):
        self.image_processor = AutoImageProcessor.from_pretrained(yolos_model)
        self.model = AutoModelForObjectDetection.from_pretrained(yolos_model)
    
    def __call__(self, image):
        inputs = self.image_processor(images=image, return_tensors="pt")
        outputs = self.model(**inputs)

        # convert outputs (bounding boxes and class logits) to COCO API
        target_sizes = torch.tensor([image.size[::-1]])
        results = self.image_processor.post_process_object_detection(outputs, threshold=0.9, target_sizes=target_sizes)[
            0
        ]

        detected_objects = []
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            box = [round(i, 2) for i in box.tolist()]
            label = self.model.config.id2label[label.item()]
            score = round(score.item(), 3)
            detected_objects.append({
                'score': score,
                'label': label,
                'box': {
                    'xmin': box[0],
                    'ymin': box[1],
                    'xmax': box[2],
                    'ymax': box[3]
                }
            })
        
        return detected_objects