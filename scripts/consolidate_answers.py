from functools import reduce

import argparse
import json
import glob
import os
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--answers_dir', '-i', default='export/answer_batches')
parser.add_argument('--output_fpath', '-o')
args = parser.parse_args()

if args.output_fpath is None:
    output_fpath = os.path.join(args.answers_dir, 'answers.json')
output_fpath = args.output_fpath

def load_json(file_path):
    with open(file_path, 'r') as fp:
        return json.loads(fp.read())

answer_file_paths = sorted(glob.glob(os.path.join(args.answers_dir, 'batch*.json')))
answer_batches = [load_json(answer_file) for answer_file in answer_file_paths]

prompt = answer_batches[0]['prompt']
assert (np.array([answer_batch['prompt'] == prompt for answer_batch in answer_batches])).all() # all batches have the same prompt

combined_data = reduce(lambda a, b: a | b, (answer_batch['data'] for answer_batch in answer_batches))

with open(output_fpath, 'w') as fp:
    json.dump({
        'prompt': prompt,
        'data': combined_data,
    }, fp, indent=4)