import jsonlines
import glob
import os

from tqdm import tqdm
from yolos import YoloDetector
from PIL import Image

detector = YoloDetector()
image_paths = sorted(glob.glob('**/*.jpg', recursive=True))

run_bbox = lambda image_path: detector(Image.open(image_path))


write_list = [{
        'image_path': image_paths[i],
        'bboxs': run_bbox(image_paths[i])
    } for i in tqdm(range(len(image_paths)))]

os.makedirs('export/bbox', exist_ok=True)
with open('export/bbox/yolos.jsonl', 'w') as fp:
    with jsonlines.Writer(fp) as writer:
        writer.write_all(write_list)