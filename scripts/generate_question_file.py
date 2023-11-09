'''
Generates questions in llava format.
Used for GPT as well.

Splits all images into three different bins
'''

import jsonlines
import os
import glob
import math

image_paths = sorted(glob.glob('**/*.jpg', recursive=True))
prompt = '''My goal is to create a detailed but accurate set of questions and answers from the image. The purpose is to create an automated VQA dataset. Pretend that you are a human thinking of questions and answers. Make sure some questions require reasoning to answer. For instance, if there is an image of a waitress bringing food to a table, a customer might be pointing at another costumer to indicate that it's their food. Create around 7 Q/A pairs.'''
questions_per_file = 50

def generate_question(image_path, question, question_id):
    return {
        'image': image_path,
        'text': question,
        'question_id': question_id,
    }

question_list = [generate_question(image_paths[i], prompt, i) for i in range(len(image_paths))]
n_files = math.ceil(len(question_list) / questions_per_file)

os.makedirs('export', exist_ok=True)
for i in range(n_files):
    start_i = i*questions_per_file
    end_i = start_i+questions_per_file

    with open(f'export/questions_{i+1}_of_{n_files}.jsonl', 'w') as fp:
        with jsonlines.Writer(fp) as writer:
            writer.write_all(question_list[start_i:end_i])
