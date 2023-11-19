from openai import OpenAI
import jsonlines
import numpy as np
import base64
import json
import os
import argparse

def get_args():
    parser = argparse.ArgumentParser(description='This program takes in a image-prompt file and returns the output of that prompt for each image.')
    parser.add_argument('prompt_file', help='Path to image-prompt file.')
    parser.add_argument('output_file', help='File path to store outputs.')
    return parser.parse_known_args()[0]

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

if __name__=="__main__":
    args = get_args()
    with open(f'{args.prompt_file}', 'r') as fp:
        with jsonlines.Reader(fp) as reader:
            question_dicts = list(reader)
            '''
            [
                {"image": "image_subset/manual-review/sa_223750.jpg", "text": "Offer a thorough analysis of the image.", "question_id": 0},
                {"image": "image_subset/manual-review/sa_223751.jpg", "text": "Offer a thorough analysis of the image.", "question_id": 1},
                ...
            ]
            '''

    image_paths = [q_dict['image'] for q_dict in question_dicts]
    prompt = question_dicts[0]['text']
    assert (np.array([q_dict['text'] == question_dicts[0]['text'] for q_dict in question_dicts])).all() # all images have the same prompt
    assert len(image_paths) <= 6 # check maximum in one prompt because gpt4vision supports a maximum of 4096 completion tokens

    client = OpenAI()

    def get_gpt_response(image_path_list):
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

    os.makedirs(os.path.dirname(args.output_file), exist_ok=True)
    response_txt = get_gpt_response(image_paths)

    try:
        image_qa_list = json.loads(response_txt[response_txt.index('```json')+len('```json'):response_txt.rindex('```')])
    except json.JSONDecodeError:
        with open(f'{args.output_file}', 'w') as fp:
            fp.write(response_txt)
        raise json.JSONDecodeError(f'JSONDecodeError raised. Outputted GPT output to {args.output_file}.')
    
    if len(image_qa_list) != len(image_paths):
        with open(f'{args.output_file}', 'w') as fp:
            fp.write(response_txt)
        
        raise AssertionError(f'GPT output length does not match the inputted image path list. Outputted GPT output to {args.output_file}.')

    # create dictionary mapping image path -> qa pairs
    ipath2qa_pairs = dict()
    for i in range(len(image_qa_list)):
        image_path = image_paths[i]
        image_qa_pairs = image_qa_list[i]
        ipath2qa_pairs[image_path] = image_qa_pairs

    # save qa pairs
    with open(f'{args.output_file}', 'w') as fp:
        fp.write(json.dumps({
            'prompt': prompt,
            'data': ipath2qa_pairs
        }, indent=4))