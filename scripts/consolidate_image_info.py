import json
import jsonlines
import os

def load_bboxs(bbox_output_fpath):
    # load bbox file
    with open(bbox_output_fpath, 'r') as fp:
        with jsonlines.Reader(fp) as reader:
            bbox_output = list(reader)
    ''' bbox_output
    [
        {
            'image_path': 'image_subset/manual-review/sa_223755.jpg',
            'bboxs': [
                {
                    'score': 0.991,
                    'label': 'person',
                    'box': {'xmin': 385.16, 'ymin': 337.4, 'xmax': 881.41, 'ymax': 1465.77}
                },
                {
                    'score': 0.943,
                    'label': 'sports ball',
                    'box': {'xmin': 1024.95, 'ymin': 1177.45, 'xmax': 1078.88, 'ymax': 1227.4}
                },
            ]
        }
    ]
    '''

    # create image -> caption map
    image2bbox = {entry['image_path']: entry['bboxs'] for entry in bbox_output}
    return image2bbox

def load_captions(llava_question_fpath, llava_answer_fpath):
    # load question file
    with open(llava_question_fpath, 'r') as fp:
        with jsonlines.Reader(fp) as reader:
            llava_question_list = list(reader)
    '''
    [
        {
            'image': 'image_subset/prompt_eng/sa_223859.jpg',
            'text': 'Offer a thorough analysis of the image.',
            'question_id': 0
        },
    ]
    '''
    assert len([entry['image'] for entry in llava_question_list]) == len(llava_question_list), 'code assumes one question per image.'
    qid2image = {entry['question_id']: entry['image'] for entry in llava_question_list} # question id -> image fpath

    # load answer file
    with open(llava_answer_fpath, 'r') as fp:
        with jsonlines.Reader(fp) as reader:
            llava_answer_list = list(reader)
    '''
    {
        'question_id': 0,
        'prompt': 'Offer a thorough analysis of the image.',
        'text': 'The image depicts a lively scene at a restaurant situated by a canal. The restaurant is filled with people enjoying their meals and conversations. There are several dining tables and chairs placed throughout the area, with some people sitting and others standing. \n\nIn addition to the people, there are multiple boats visible in the scene, both near the restaurant and further away. Some boats are docked close to the restaurant, while others are floating on the canal. The presence of boats adds to the overall ambiance of the location, making it an attractive spot for people to dine and relax.',
        'answer_id': 'AHZtwcCjjXdcF84MHcgggb',
        'model_id': 'llava-v1.5-7b',
        'metadata': {}
    }
    '''
    assert len(llava_answer_list) == len(llava_question_list), 'matched question/answer files should be the same length.'
    qid2caption = {entry['question_id']: entry['text'] for entry in llava_answer_list}

    # create image -> caption map
    assert qid2caption.keys() == qid2image.keys()
    image2caption = {qid2image[qid]: qid2caption[qid] for qid in qid2caption.keys()}
    return image2caption

bbox_output_fpath = 'dev_input/bboxs/yolos.jsonl'

llava_question_fpath = 'dev_input/llava/questions.jsonl'
llava_answer_fpath = 'dev_input/llava/llava-v1.5-7b.jsonl'

bboxs = load_bboxs(bbox_output_fpath)
captions = load_captions(llava_question_fpath, llava_answer_fpath)
images = set(bboxs.keys()).intersection(captions.keys())

if len(bboxs) != len(captions):
    print(f'Warning: bboxs has {len(bboxs)} elements while captions has {len(captions)}. Only the intersection ({len(images)} elements) will be used.')

image_info = {
    image: {
        'caption': captions[image],
        'bboxs': bboxs[image],
    } for image in images
}

os.makedirs('export', exist_ok=True)
image_info_json = json.dumps(image_info)
with open('export/image_info.json', 'w') as fp:
    fp.write(image_info_json)