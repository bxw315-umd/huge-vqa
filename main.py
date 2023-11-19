import subprocess
import argparse
import glob
import os

from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--prompt_file', '-p', required=True)
parser.add_argument('--image_root', '-r', required=True)

args = parser.parse_args()
prompt_file = args.prompt_file
image_root = args.image_root

if os.path.exists('export'):
    print('Please delete the existing export folder to prevent overwriting data.')
else:
    # generate question files containing the prompt
    print('Generating question files...')
    subprocess.run(f'python scripts/generate_question_file.py -i {prompt_file} -r {image_root} -q 6')

    # run the question files
    print('Running question files through GPT...')
    answer_file = lambda question_fpath: question_fpath.replace('questions', 'answers')[:-1] # function to convert question fpath to corresponding answer fpath

    question_files = sorted(glob.glob('export/questions/*.jsonl'))
    for question_file in tqdm(question_files):
        subprocess.run(f'python scripts/run_questions.py {question_file} {answer_file(question_file)}')

    print('Consolidating answers into one file...')
    # consolidate answers into one file
    subprocess.run(f'python scripts/consolidate_answers.py')