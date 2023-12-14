'''
generate_batches.py

Authors: Benjamin Wu & Tomer Atzili
Date: 12/13/2023

This program serves to take images and turn them into json files that can be taken by run_batch.py to make API calls and generate Q/A pairs.
It takes in an image folder to retrieve images from and a batch size - the number of requests to the GPT API one wants to call at once.
It will use this information to create files with the right number of image paths so that the desired number of requests is in each.
Each request includes multiple images, as defined by question_sets_per_file.
'''

import argparse
import glob
import json
import os

def generate_batch(image_list, images_per_request):
    '''Separate image_list into batches of `images_per_request`
    e.g. [1,2,3,4,5,6,7,8,9] becomes [[1,2,3],[4,5,6],[7,8,9]] with images_per_request=3'''
    return [image_list[i:i+images_per_request] for i in range(0, len(image_list), images_per_request)]

def parse_arguments():
    '''Parse arguments as dictated by the argument parser.'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_folder', '-i', required=True, help='Path to the root directory containing .png images.')
    parser.add_argument('--batch_size', '-b', default=80, help='Number of batches (and therefore gpt4 requests) within a batch file. MUST BE <=100 DUE TO CURRENT API LIMITS')
    return parser.parse_args()

def generate_batches(image_folder, batch_size):
    '''Take in the image folder and batch size from the argument parser.
    batches is a list  of the lists outputted by generate_batch(), with one of such lists per file.
    e.g. If you have 200 images, 5 images per request, and a batch size of 10: 
    There will be 50 images per file outputted. Each of these 4 files will store 10 lists of 5 image paths (each of these makes up an API request).'''
    image_folder = image_folder
    batch_size = batch_size

    image_paths = sorted(glob.glob(os.path.join(image_folder, '**/*.jpg'), recursive=True))
    images_per_request = 6 # Set as 6 because of gpt4vision API token limit of 4096 - we have no testing/debug support for images > 6

    question_sets_per_file = images_per_request*batch_size

    batches = [generate_batch(image_paths[i:i+question_sets_per_file], images_per_request) for i in range(0, len(image_paths), question_sets_per_file)]
    return batches

def save_batches(batches, root_path='export/question_batches'):
    '''Saves each element in batches into a separate file at root_path/batch_i_of_totalfiles'''
    os.makedirs(root_path, exist_ok=True)
    for i in range(len(batches)):
        path = os.path.join(root_path, f'batch_{i+1}_of_{len(batches)}.json')
        with open(path, 'w') as fp:
            json.dump(batches[i], fp, indent=4)

if __name__ == '__main__':
    args = parse_arguments()
    batches = generate_batches(args.image_folder, int(args.batch_size))
    save_batches(batches)

