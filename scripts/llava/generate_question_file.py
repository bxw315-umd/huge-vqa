import jsonlines
import os
import glob

image_paths = glob.glob('**/*.jpg', recursive=True)
question = 'Offer a thorough analysis of the image.'

def generate_question(image_path, question, question_id):
    return {
        'image': image_path,
        'text': question,
        'question_id': question_id,
    }

question_list = [generate_question(image_paths[i], question, i) for i in range(len(image_paths))]

os.makedirs('llava', exist_ok=True)
with open('llava/questions.jsonl', 'w') as fp:
    with jsonlines.Writer(fp) as writer:
        writer.write_all(question_list)