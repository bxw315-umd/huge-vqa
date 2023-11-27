from openai import OpenAI
from multiprocessing import Pool
from functools import reduce
from tqdm import tqdm
import numpy as np
import base64
import json
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--batch_fpath', '-b', required=True)
parser.add_argument('--prompt_fpath', '-p', required=True)
parser.add_argument('--output_fpath', '-o', required=True)
parser.add_argument('--debug_dir', '-d')
args = parser.parse_args()

batch_fpath = args.batch_fpath
output_fpath = args.output_fpath
prompt_fpath = args.prompt_fpath
debug_dir = args.debug_dir

if debug_dir is None:
    debug_dir = os.path.dirname(output_fpath)

def encode_image(image_path):
    '''encodes an image into base64'''
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_gpt_response(image_path_list):
    '''sends the prompt and the list of images to gpt. returns the text response.'''
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", 
                        "text": prompt
                    },
                ] + [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encode_image(image_path)}",
                            "detail": "low",
                        }
                    } for image_path in image_path_list
                ],
            }
        ],
        max_tokens=600*len(image_path_list),
    )

    return response.choices[0].message.content

# load in image batches
with open(batch_fpath, 'r') as fp:
    image_batches = json.load(fp)

# load in prompt
with open(prompt_fpath, 'r') as fp:
    prompt = fp.read()

client = OpenAI()

def run_image_batch(batch_id):
    '''
    returns a dictionary of image_path -> q/a pairs for a single batch (currently 6 images)
    '''
    batch = image_batches[batch_id]

    # run batch through gpt
    response_txt = get_gpt_response(batch)

    try:
        image_qa_list = json.loads(response_txt[response_txt.index('```json')+len('```json'):response_txt.rindex('```')])
    except Exception as e:
        # if parsing fails, output the response text for debugging
        # save gpt response to file w/ batch_id
        answer_name, answer_ext = os.path.splitext(os.path.basename(output_fpath))
        os.makedirs(debug_dir, exist_ok=True)

        debug_fpath = os.path.join(debug_dir, f'debug_batch{batch_id}_{answer_name}{answer_ext}')
        with open(debug_fpath, 'w') as fp:
            json.dump({
                'batch_fpath': batch_fpath,
                'batch_id': batch_id,
                'error': str(e),
                'response': response_txt,
            }, fp, indent=4)
        print(f"Failed to parse GPT JSON output. Wrote response to {debug_fpath}.")
        raise e

    # create image path->qa list dict
    ipath2qa_pairs = dict()
    for i in range(len(image_qa_list)):
        image_path = batch[i]
        image_qa_pairs = image_qa_list[i]
        ipath2qa_pairs[image_path] = image_qa_pairs
    return ipath2qa_pairs

def run_batch_safe(batch_id):
    try:
        return run_image_batch(batch_id)
    except Exception as e:
        print(e)
        return dict()

# multiprocessing disabled because of tokens per minute rate limit (10,000). in the future, consider exponential backoff
# with tqdm(total=len(image_batches), miniters=1) as loading_bar:
#     with Pool() as p:
#         data_dicts = []
#         for result in p.imap_unordered(run_batch_safe, range(len(image_batches))):
#             data_dicts.append(result)
#             loading_bar.update()

data_dicts = [run_batch_safe(i) for i in tqdm(range(len(image_batches)))]

ipath2qa_pairs = reduce(lambda a, b: a | b, data_dicts)

# save qa pairs
os.makedirs(os.path.dirname(output_fpath), exist_ok=True)
with open(output_fpath, 'w') as fp:
    fp.write(json.dumps({
        'prompt': prompt,
        'data': ipath2qa_pairs
    }, indent=4))