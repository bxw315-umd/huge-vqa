from functools import reduce

import argparse
import json
import glob
import os
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--answers_dir', default='export/answers')
args = parser.parse_args()

def load_json(file_path):
    with open(file_path, 'r') as fp:
        return json.loads(fp.read())

answer_file_paths = sorted(glob.glob(os.path.join(args.answers_dir, '*.json')))
answer_batches = [load_json(answer_file) for answer_file in answer_file_paths]

prompt = answer_batches[0]['prompt']
assert (np.array([answer_batch['prompt'] == prompt for answer_batch in answer_batches])).all() # all batches have the same prompt

combined_data = reduce(lambda a, b: a | b, (answer_batch['data'] for answer_batch in answer_batches))

with open(os.path.join(args.answers_dir, 'answers.json'), 'w') as fp:
    json.dump({
        'prompt': prompt,
        'data': combined_data,
    }, fp, indent=4)