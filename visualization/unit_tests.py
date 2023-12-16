'''
unit_tests.py

Authors: Benjamin Wu & Tomer Atzili
Date: 12/13/2023

A testing suite for the visualization script.
'''
import unittest
import tempfile
import shutil
import os
from unittest.mock import MagicMock, patch, mock_open
import json
from app import ImageInfo

class TestApp(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()

        qa_dicts = {
            'image_subset/images/sa_234937.jpg': [{'question': 'What might be the cultural significance of the place where the people are walking?', 'answer': 'The intricate tile work and the architectural design suggest that it is a place of historical or cultural significance, possibly a religious or heritage site.'}, \
                    {'question': 'Based on the clothing of the individuals, what is the likely weather in the image?', 'answer': 'The weather appears to be cool or mild, as most individuals are wearing long sleeves and pants.'}, \
                    {'question': 'What can be inferred about the popularity of the location?', 'answer': 'The location seems to be popular, as there are several groups of people visiting, indicating it might be a tourist attraction or a place of interest.'}, \
                    {'question': 'Considering the design of the buildings, what region or culture might it represent?', 'answer': 'The blue tiles and domed structures suggest that the architecture may be of Islamic influence, likely representing Middle Eastern or Central Asian culture.'}, \
                    {'question': 'How do the individuals in the image appear to be engaged with the location?', 'answer': 'The individuals are walking and observing their surroundings, implying they are visitors or tourists exploring the site.'}, \
                    {'question': 'Judging by the path and layout, what is the likely purpose of this corridor?', 'answer': 'The corridor likely serves as a pedestrian walkway guiding visitors between different sections of the historic or cultural site.'}, \
                    {'question': 'What time of day does it appear to be in the image?', 'answer': 'Given the natural light and shadows, it seems to be daytime, possibly late morning or early afternoon.'}], 
            'image_subset/images/sa_234938.jpg': [{'question': 'What does the scenery around the individual suggest about the location?', 'answer': 'The lush greenery, rice fields, and mountain in the background suggest a rural, tropical environment, possibly in Southeast Asia.'}, \
                    {'question': 'What activity is the person in the image most likely doing?', 'answer': 'The person seems to be walking down a path, likely hiking or exploring the rural landscape.'}, {'question': 'Considering the walking path, what is its likely purpose in this setting?', 'answer': 'The walking path is most likely intended for touring or exploring the rice fields and the surrounding natural landscape.'}, \
                    {'question': 'Based on the image, what can be deduced about the time of year?', 'answer': 'The verdant fields and clear weather suggest it might be during a growing season and not the dry or cold season.'}, {'question': 'How does the attire of the person suggest preparedness for the setting?', 'answer': "The person's attire including a backpack and comfortable clothing indicates they are prepared for outdoor activities like hiking or walking."}, \
                    {'question': "What might be the benefit of the walkway's design in this environment?", 'answer': 'The raised brick walkway helps visitors traverse the area without disturbing the rice fields and protects them from wet ground.'}, {'question': 'What can be said about the weather at the moment in the photograph?', 'answer': 'The weather seems fair with a mix of sun and clouds, ideal for outdoor activities like walking or hiking.'}]}

        self.answers = {
            'prompt': 'Generate a Q/A pair list.',
            'data': qa_dicts,
        }

        self.answers_fpath = f'{self.test_dir}/answers.json'

        with open(self.answers_fpath, 'w') as fp:
            json.dump(self.answers, fp)

        self.image_info = ImageInfo(self.answers_fpath)

    def tearDown(self):
        # Remove the temporary directory after testing
        shutil.rmtree(self.test_dir)

    def test_invalid_path(self):
        self.assertEqual(self.image_info.get_qa('fake_path'), [])
    
    def test_get_image_fpaths(self):
        self.assertEqual(self.image_info.get_image_fpaths(), list(self.answers['data'].keys()))
    
    def test_get_qa_pairs(self):
        for image_fpath in self.answers['data'].keys():
            qa_tuples = self.image_info.get_qa(image_fpath) # list of Q/A tuples
            qa_dicts = self.answers['data'][image_fpath] # list of Q/A dicts

            self.assertEqual(len(qa_tuples), len(qa_dicts))
            for qa_dict in qa_dicts:
                self.assertTrue((qa_dict['question'], qa_dict['answer']) in qa_tuples)

    def test_bad_qa_pair(self):
        answers_fpath = f'{self.test_dir}/bad_answers.json'
        with open(answers_fpath, 'w') as fp:
            json.dump({'prompt': 'p', 'data': {'image.png': {'Quest.': 'q', 'Ans.': 'a'}}}, fp)

        self.assertEqual(ImageInfo(answers_fpath).get_qa('image.png'), [])


if __name__ == '__main__':
    unittest.main()