'''
app.py

Authors: Benjamin Wu & Tomer Atzili
Date: 12/13/2023

This program visualizes an answers.json output by providing a webpage that 
displays images alongside their Q/A pairs. 
'''

import cv2
import json
import re
import argparse
from flask import (
    Flask, 
    make_response, 
    request, 
    render_template, 
    abort
)

class ImageInfo:
    '''
    Stores Q/A information contained in answers.json outputs.
    Expects a JSON file containing a dict with keys 'prompt', containing a string,
    and 'data', a dictionary where image filepaths map to a list of question/answer dictionaries.
    '''

    def __init__(self, image_info_fpath):
        # load answer file
        with open(image_info_fpath, 'r') as fp:
            answer_file = json.loads(fp.read())
        
        self.prompt = answer_file['prompt']
        self.image_info = answer_file['data']
    
    def get_qa(self, image_fpath):
        '''
        Returns a list of (question, answer) tuples representing the Q/A pairs for the image.
        If the Q/A pairs can't be read, returns an empty list
        '''
        if image_fpath not in self.image_info:
            return []

        get_qa = lambda qa_dict: (qa_dict['question'], qa_dict['answer'])
        rekey_dict = lambda qa_dict: {k.lower(): v for k, v in qa_dict.items()} #  handle casing, i.e. question and Question are both accepted

        try:
            match_list = [get_qa(rekey_dict(qa_dict)) for qa_dict in self.image_info[image_fpath]]
            return match_list
        except:
            return []
    
    def get_image_fpaths(self):
        '''
        Returns a list of all image_fpaths stored in this object.
        '''
        return list(self.image_info.keys())

app = Flask(__name__)

@app.route('/')
def show_index():
    # shows a page containing images with Q/A pairs in a table
    image_fpaths = [image_fpath for image_fpath in image_info.get_image_fpaths()]
    image_links = [f'/image?image_fpath={image_fpath}' for image_fpath in image_info.get_image_fpaths()]
    qa_pairs = [image_info.get_qa(image_fpath) for image_fpath in image_info.get_image_fpaths()]
    prompt = image_info.prompt

    return render_template("index.html", data=zip(image_fpaths, image_links, qa_pairs), prompt=prompt)

@app.route('/image', methods=['GET'])
def image():
    # serves .png images from the local filesystem
    image_fpath = request.args.get('image_fpath').replace('\\', '/')
    img = cv2.imread(image_fpath)

    if img is None:
        abort(404)

    retval, buffer = cv2.imencode('.png', img)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/png'
    return response

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--answers_fpath', '-i', default='export/answers.json', help='File path of answers.json file to visualize.')
    args = parser.parse_args()

    image_info = ImageInfo(args.answers_fpath)
    app.run(debug=True)