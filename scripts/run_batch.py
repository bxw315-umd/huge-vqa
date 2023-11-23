from openai import OpenAI
import numpy as np
import base64
import json
import os
import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument('--batch_fpath', '-b', required=True)
# parser.add_argument('--prompt_fpath', '-p', required=True)
# args = parser.parse_args()

batch_fpath = 'export/question_batches/batch_1_of_3.json'
prompt_fpath = 'prompts/current.txt'

def encode_image(image_path):
    '''encodes an image into base64'''
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_gpt_response(image_path_list):
    '''sends the prompt and the list of images to gpt. returns the text response.'''
    return "i'm a fill in"
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

# start of function
batch_id = 0
batch = image_batches[batch_id]

# run batch through gpt
# save gpt response to file w/ batch_id
# decode gpt json output
# create image path->qa list dict
# return dict

client = OpenAI()