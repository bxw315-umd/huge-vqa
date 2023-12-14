'''
consolidate_answers.py

Authors: Benjamin Wu & Tomer Atzili
Date: 12/13/2023

This program serves to find answer batch files saved by run_batch.py in the answers directory. It will take all of the data in these batch files
and consolidate them into a single json. This json, along with the images, will comprise a huge VQA dataset.
'''

from functools import reduce

import argparse
import json
import glob
import os
import numpy as np

def parse_arguments():
    '''Parse arguments as dictated by the argument parser.'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--answers_dir', '-i', default='export/answer_batches')
    parser.add_argument('--output_fpath', '-o')
    args = parser.parse_args()
    return args

def load_json(file_path):
    with open(file_path, 'r') as fp:
        return json.loads(fp.read())

def consolidate(args):
    '''Combines data from all batch*.json files in the answers_dir argument provided.
    It checks that all the batches have the same GPT prompt and returns that prompt.
    Also returns a set of all data from the batch files.'''
    answer_file_paths = sorted(glob.glob(os.path.join(args.answers_dir, 'batch*.json')))
    answer_batches = [load_json(answer_file) for answer_file in answer_file_paths]

    prompt = answer_batches[0]['prompt']
    assert (np.array([answer_batch['prompt'] == prompt for answer_batch in answer_batches])).all() # all batches have the same prompt

    combined_data = reduce(lambda a, b: a | b, (answer_batch['data'] for answer_batch in answer_batches))
    return (prompt, combined_data)

def save_consolidated(args, prompt, combined_data):
    '''Saves the prompt and combined data returned from consolidate() in answers_dir/answers.json or in a specified output path.'''
    if args.output_fpath is None:
        output_fpath = os.path.join(args.answers_dir, 'answers.json')
    else:
        output_fpath = args.output_fpath
    with open(output_fpath, 'w') as fp:
        json.dump({
            'prompt': prompt,
            'data': combined_data,
        }, fp, indent=4)

if __name__ == '__main__':
    args = parse_arguments()
    prompt, combined_data = consolidate(args)
    save_consolidated(args, prompt, combined_data)