from openai import OpenAI
import jsonlines
import numpy as np
import json
import glob
import os
import argparse

from tqdm import tqdm


def get_args():
    parser = argparse.ArgumentParser(description='This program takes in a image-prompt file and returns the output of that prompt for each image.')
    parser.add_argument('prompt_file', help='Path to image-prompt file.')
    parser.add_argument('output_file', help='File path to store outputs.')
    return parser.parse_known_args()[0]

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

    # get image urls
    replace_slashes = lambda img_path: img_path.replace('\\', '/')
    add_base_url = lambda img_path: 'https://raw.githubusercontent.com/bxw315-umd/huge-vqa/main/' + str(img_path)
    ipath2url = {img_path: add_base_url(replace_slashes(img_path)) for img_path in image_paths}

    client = OpenAI()

    def get_gpt_caption(image_url):
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url,
                                "detail": "low",
                            }
                        },
                    ],
                }
            ],
            max_tokens=600,
        )

        return response.choices[0].message.content

    ipath2caption = dict()
    os.makedirs('export/gpt', exist_ok=True)
    def save_data():
        to_save = {
            'prompt': prompt,
            'data': ipath2caption
        }

        with open(f'{args.output_file}', 'w') as fp:
            fp.write(json.dumps(to_save, indent=4))

    i=1
    for ipath, url in tqdm(ipath2url.items()):
        ipath2caption[ipath] = get_gpt_caption(url)
        if(i%10 == 0):
            save_data()
        i+=1
    save_data()

