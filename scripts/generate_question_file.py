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

#Reads prompt from specified file.
with open(args.input_prompt_fpath, 'r') as f:
    prompt = f.read()
#Test prompt is a string with length > 0
assert isinstance(prompt, str) and len(prompt) > 0, "Invalid prompt."

#Recursively retrieve all jpg files under the image root specified.
image_paths = sorted(glob.glob(os.path.join(args.image_root, '**/*.jpg'), recursive=True))
#Check that there are images found
assert len(image_paths) > 0, "No images found."

questions_per_file = int(args.questions_per_file)

#Method to create a dictionary for each image. The question parameter is just the prompt and the id's begin at 0 befor incrementing.
def generate_question(image_path, question, question_id):
    return {
        'image': image_path,
        'text': question,
        'question_id': question_id,
    }

#Creates a list of dictionaries generated for each image via generate_question().
question_list = [generate_question(image_paths[i], prompt, i) for i in range(len(image_paths))]
#Test to see if list is the right length
assert len(question_list) == len(image_paths)
#Test the first entry
entry = question_list[0]
assert entry['image'] != None and entry['text'] != None and entry['question_id'] == 0
assert entry['image'][-4:] == ".jpg", "Images are in incorrect format."

n_files = math.ceil(len(question_list) / questions_per_file)

#Saves questions from question_list into jsonl files readable by API script.
root_path = 'export/questions'
os.makedirs(root_path, exist_ok=True)
for i in range(n_files):
    start_i = i*questions_per_file
    end_i = start_i+questions_per_file

    with open(os.path.join(root_path, f'questions_{i+1}_of_{n_files}.jsonl'), 'w') as fp:
        with jsonlines.Writer(fp) as writer:
            writer.write_all(question_list[start_i:end_i])
#Assert files are created
check_files_list = sorted(glob.glob(os.path.join(root_path, '*.jsonl'), recursive=True))
assert len(check_files_list) >= n_files
for i in range(n_files):
    assert (f'{root_path}/questions_{i+1}_of_{n_files}.jsonl') in check_files_list, "Question files are missing."