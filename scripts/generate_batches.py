import argparse
import glob
import json
import os

parser = argparse.ArgumentParser()
parser.add_argument('--image_folder', '-i', required=True, help='Path to the root directory containing .png images.')
parser.add_argument('--batch_size', '-b', default=80, help='Number of batches (and therefore gpt4 requests) within a batch file.')
args = parser.parse_args()

image_folder = args.image_folder
batch_size = int(args.batch_size)

image_paths = sorted(glob.glob(os.path.join(image_folder, '**/*.jpg'), recursive=True))
questions_per_batch = 6 # hard-coded because of gpt4vision token limit of 4096

n_batches_per_file = batch_size
questions_per_file = questions_per_batch*n_batches_per_file

def generate_batches(image_list):
    '''separate image_list into batches of `questions_per_batch`
    e.g. [1,2,3,4,5,6,7,8,9] becomes [[1,2,3],[4,5,6],[7,8,9]] with questions_per_batch=3'''
    return [image_list[i:i+questions_per_batch] for i in range(0, len(image_list), questions_per_batch)]

batches = [generate_batches(image_paths[i:i+questions_per_file]) for i in range(0, len(image_paths), questions_per_file)]

root_path = 'export/question_batches'
os.makedirs(root_path, exist_ok=True)
for i in range(len(batches)):
    with open(os.path.join(root_path, f'batch_{i+1}_of_{len(batches)}.json'), 'w') as fp:
        json.dump(batches[i], fp, indent=4)