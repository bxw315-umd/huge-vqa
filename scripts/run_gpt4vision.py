from openai import OpenAI
import json
import glob
import os

from tqdm import tqdm

# get image urls
image_paths = sorted(glob.glob('**/*.jpg', recursive=True))
replace_slashes = lambda img_path: img_path.replace('\\', '/')
add_base_url = lambda img_path: 'https://raw.githubusercontent.com/bxw315-umd/huge-vqa/main/' + str(img_path)
ipath2url = {img_path: add_base_url(replace_slashes(img_path)) for img_path in image_paths}
prompt = "Describe this image in detail."

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
        max_tokens=300,
    )

    return response.choices[0].message.content

ipath2caption = dict()

for ipath, url in tqdm(ipath2url.items()):
    ipath2caption[ipath] = get_gpt_caption(url)

to_save = {
    'prompt': prompt,
    'data': ipath2caption
}

os.makedirs('export/gpt', exist_ok=True)
with open('export/gpt/gpt_captions.json', 'w') as fp:
    fp.write(json.dumps(to_save))