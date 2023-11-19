'''
Generates questions in llava format.
Used for GPT as well.

Splits all images into three different bins
'''

import argparse
import jsonlines
import os
import glob
import math

parser = argparse.ArgumentParser()
parser.add_argument('--input_prompt_fpath', '-i', required=True)
parser.add_argument('--image_root', '-r', default='.')
parser.add_argument('--questions_per_file', '-q', default=50)
args = parser.parse_args()

with open(args.input_prompt_fpath, 'r') as f:
    prompt = f.read()

image_paths = sorted(glob.glob(os.path.join(args.image_root, '**/*.jpg'), recursive=True))
questions_per_file = int(args.questions_per_file)

def generate_question(image_path, question, question_id):
    return {
        'image': image_path,
        'text': question,
        'question_id': question_id,
    }

question_list = [generate_question(image_paths[i], prompt, i) for i in range(len(image_paths))]
n_files = math.ceil(len(question_list) / questions_per_file)

root_path = 'export/questions'
os.makedirs(root_path, exist_ok=True)
for i in range(n_files):
    start_i = i*questions_per_file
    end_i = start_i+questions_per_file

    with open(os.path.join(root_path, f'questions_{i+1}_of_{n_files}.jsonl'), 'w') as fp:
        with jsonlines.Writer(fp) as writer:
            writer.write_all(question_list[start_i:end_i])
