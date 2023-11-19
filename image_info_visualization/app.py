# TODO Q/A pairs in table

import cv2
import json
import re
from flask import (
    Flask, 
    make_response, 
    request, 
    render_template, 
    abort
)

class ImageInfo:
    '''
    Stores caption and bounding box information.
    '''

    '''
    {
        "prompt": "My goal is to create a detailed but accurate set of questions and answers from the image. The purpose is to create an automated VQA dataset. Pretend that you are a human thinking of questions and answers. Make sure some questions require reasoning to answer. For instance, if there is an image of a waitress bringing food to a table, a customer might be pointing at another costumer to indicate that it's their food. Create around 7 Q/A pairs. Provide your Q/A pairs in JSON format.", 
        "data": {
            "image_subset\\manual-review\\sa_223753.jpg": "```json\n[\n  {\n    \"question\": \"What type of location is depicted in the image?\",\n    \"answer\": \"The image shows a beach volleyball court.\"\n  },\n  {\n    \"question\": \"What type of trees are visible behind the volleyball court?\",\n    \"answer\": \"There are palm trees visible behind the volleyball court.\"\n  },\n  {\n    \"question\": \"What is the color of the volleyball net?\",\n    \"answer\": \"The volleyball net is blue.\"\n  },\n  {\n    \"question\": \"Is the volleyball court currently in use?\",\n    \"answer\": \"No, the volleyball court is not currently in use as there are no players visible.\"\n  },\n  {\n    \"question\": \"Can you deduce the weather condition in the image?\",\n    \"answer\": \"The weather appears to be sunny as there are shadows on the ground and the sky is clear.\"\n  },\n  {\n    \"question\": \"Are there any buildings in the image?\",\n    \"answer\": \"Yes, there appears to be a building partially visible through the trees in the background.\"\n  },\n  {\n    \"question\": \"Judging by the appearance of the scene, where might this location be?\",\n    \"answer\": \"Given the palm trees and sandy court, this location might be in a tropical or subtropical region.\"\n  }\n]\n```"},
            ...
        }
    '''

    def __init__(self, image_info_fpath):
        # load answer file
        with open(image_info_fpath, 'r') as fp:
            answer_file = json.loads(fp.read())
        
        self.prompt = answer_file['prompt']
        self.image_info = answer_file['data']

    def get_text(self, image_fpath):
        if image_fpath not in self.image_info:
            return 'Text not found in answers file.'
        return self.image_info[image_fpath]
    
    def get_qa(self, image_fpath):
        if image_fpath not in self.image_info:
            return 'Text not found in answers file.'
        match_list = [(qa_dict['question'], qa_dict['answer']) for qa_dict in self.image_info[image_fpath]]
        # match_list of format ('What is the person wearing a headscarf holding in her hand?', 'She is holding a piece of paper or a card.')
        return match_list

image_info = ImageInfo('export/answers/answers.json')
app = Flask(__name__)

@app.route('/')
def show_index():
    image_fpaths = [f'/image?image_fpath={image_fpath}' for image_fpath in image_info.image_info]
    captions = [image_info.get_text(image_fpath) for image_fpath in image_info.image_info]
    qa_pairs = [image_info.get_qa(image_fpath) for image_fpath in image_info.image_info]
    prompt = image_info.prompt

    return render_template("index.html", data=zip(image_fpaths, captions, qa_pairs), prompt=prompt)

@app.route('/image', methods=['GET'])
def image():
    image_fpath = request.args.get('image_fpath').replace('\\', '/')
    img = cv2.imread(image_fpath)

    if img is None:
        abort(404)

    retval, buffer = cv2.imencode('.png', img)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/png'
    return response