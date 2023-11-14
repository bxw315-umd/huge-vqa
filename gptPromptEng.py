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
prompt = "My goal is to create a detailed but accurate set of questions and answers from the image. The purpose is to create an automated VQA dataset. \
    Pretend that you are a human thinking of questions and answers. Make sure some questions require reasoning to answer. For instance, if there is an image of \
    a waitress bringing food to a table, a customer might be pointing at another costumer to indicate that it's their food. Create around 7 Q/A pairs."
print(ipath2url['image_subset/manual-review/sa_223750.jpg'])
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

#print(get_gpt_caption(ipath2url['image_subset/manual-review/sa_223750.jpg']))

ipath2caption = dict()
i=0
for ipath, url in tqdm(ipath2url.items()):
    #ipath2caption[ipath] = get_gpt_caption(url)
    to_save = {
    'prompt': prompt,
    'data': ipath2caption
    }
    i+=1



os.makedirs('export/gpt', exist_ok=True)
with open('export/gpt/gpt_captions.json', 'w') as fp:
    fp.write(json.dumps(to_save))