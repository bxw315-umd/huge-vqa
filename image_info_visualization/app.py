import cv2
import json
from flask import Flask, make_response, request, render_template

class ImageInfo:
    '''
    Stores caption and bounding box information.
    '''

    '''
    {
        'image': 'image_subset/manual-review/sa_223755.jpg',
        'caption': 'The image depicts a group of people walking down a sidewalk in a park. Among them, two women are walking past a bench, and one of them is wearing a face mask. The park is surrounded by trees, creating a pleasant and relaxing atmosphere.\n\nThere are several other people in the scene, some of them carrying handbags. A few benches are visible in the park, with one near the center of the image and another further back. The presence of multiple people and the park setting suggest that this could be a popular spot for outdoor activities and socializing.',
        'bboxs': [
            {
                'score': 0.995,
                'label': 'person',
                'box': {'xmin': 513.64, 'ymin': 335.29, 'xmax': 867.84, 'ymax': 1463.29}
            },
            {
                'score': 0.998,
                'label': 'person',
                'box': {'xmin': 182.44, 'ymin': 424.95, 'xmax': 624.14, 'ymax': 1317.45}
            },
        ]
    }
    '''

    def __init__(self, image_info_fpath):
        # load answer file
        with open(image_info_fpath, 'r') as fp:
            self.image_info = json.loads(fp.read())
    
    def get_caption(self, image_fpath):
        if image_fpath not in self.image_info:
            return None
        return self.image_info[image_fpath]['caption']
    
    def get_bboxs(self, image_fpath):
        if image_fpath not in self.image_info:
            return None
        return self.image_info[image_fpath]['bboxs']

image_info = ImageInfo('export/image_info.json')
app = Flask(__name__)

@app.route('/')
def show_index():
    image_fpath = request.args.get('image_fpath')
    caption = image_info.get_caption(image_fpath)
    return render_template("index.html", user_image=f'/image?image_fpath={image_fpath}', caption=caption)

@app.route('/image', methods=['GET'])
def image():
    image_fpath = request.args.get('image_fpath')
    img = cv2.imread(image_fpath)

    retval, buffer = cv2.imencode('.png', img)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/png'
    return response