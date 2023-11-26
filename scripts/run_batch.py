from openai import OpenAI
from functools import reduce
from tqdm import tqdm
import numpy as np
import base64
import json
import os
import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument('--batch_fpath', '-b', required=True)
# parser.add_argument('--prompt_fpath', '-p', required=True)
# parser.add_argument('--output_fpath', '-o', required=True)
# args = parser.parse_args()

batch_fpath = 'export/question_batches/batch_1_of_3.json'
output_fpath = 'export/answer_batches/batch_1_of_3.json'
prompt_fpath = 'prompts/current.txt'

def encode_image(image_path):
    '''encodes an image into base64'''
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_gpt_response(image_path_list):
    '''sends the prompt and the list of images to gpt. returns the text response.'''
    return '```json \n' + json.dumps([{'question': 'Q?', 'answer': 'A.'} for image in image_path_list]) + '   ```'
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

# start of function
def run_batch(batch_id):
    '''
    returns a dictionary of image_path -> q/a pairs for a single batch (currently 6 images)
    '''
    batch = image_batches[batch_id]

    # run batch through gpt
    response_txt = get_gpt_response(batch)

    # save gpt response to file w/ batch_id
    answer_folder = os.path.dirname(output_fpath)
    answer_name, answer_ext = os.path.splitext(os.path.basename(output_fpath))
    os.makedirs(answer_folder, exist_ok=True)

    try:
        image_qa_list = json.loads(response_txt[response_txt.index('```json')+len('```json'):response_txt.rindex('```')])
    except json.JSONDecodeError:
        # if parsing fails, output the response text for debugging
        debug_fpath = os.path.join(answer_folder, f'{answer_name}_batch{batch_id}{answer_ext}')
        with open(debug_fpath, 'w') as fp:
            json.dump({
                'prompt_fpath': prompt_fpath,
                'batch_fpath': batch_fpath,
                'response': response_txt,
            }, fp)
        raise json.JSONDecodeError(f"Failed to parse GPT JSON output. Outputted debug information to {debug_fpath}.")

    # create image path->qa list dict
    ipath2qa_pairs = dict()
    for i in range(len(image_qa_list)):
        image_path = batch[i]
        image_qa_pairs = image_qa_list[i]
        ipath2qa_pairs[image_path] = image_qa_pairs
    return ipath2qa_pairs

ipath2qa_pairs = reduce(lambda a, b: a | b, [run_batch(i) for i in tqdm(range(len(image_batches)))])

# save qa pairs
with open(output_fpath, 'w') as fp:
    fp.write(json.dumps({
        'prompt': prompt,
        'data': ipath2qa_pairs
    }, indent=4))