'''
unit_tests.py

Authors: Benjamin Wu & Tomer Atzili
Date: 12/13/2023

A testing suite for all other scripts. Each class is set up to test a different file. There is dummy data (varying degrees of closeness to real data) that
is put into the major functions of each script. The output is then tested.
'''
import unittest
import tempfile
import shutil
import os
from generate_batches import generate_batches, save_batches
from unittest.mock import MagicMock, patch, mock_open
import json
from run_batch import (
    run_image_batch,
    run_batch_safe,
    run,
    save_batch
)
from consolidate_answers import parse_arguments, consolidate, save_consolidated

class TestImageBatchGeneration(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the temporary directory after testing
        shutil.rmtree(self.test_dir)

    def test_full_process(self):
        # Create some dummy image files for testing
        dummy_image_paths = [os.path.join(self.test_dir, f'image_{i}.jpg') for i in range(1, 26)]
        for path in dummy_image_paths:
            with open(path, 'w') as f:
                f.write("Dummy image content")

        # Call the main processing functions
        batches = generate_batches(self.test_dir, 2)
        save_batches(batches, root_path=self.test_dir)

        # Verify the generated batches
        self.assertEqual(len(batches), 3)  # Adjust this based on your specific test case

        # Verify the saved batches
        for i in range(len(batches)):
            batch_path = os.path.join(self.test_dir, f'batch_{i+1}_of_{len(batches)}.json')
            self.assertTrue(os.path.exists(batch_path))

class TestRunBatch(unittest.TestCase):

    def setUp(self):
        self.mock_openai = MagicMock()
        self.mock_response = MagicMock()
        self.mock_response.choices[0].message.content = '```json\
[\
  [\
    {\
      "question": "What might be the cultural significance of the place where the people are walking?",\
      "answer": "The intricate tile work and the architectural design suggest that it is a place of historical or cultural significance, possibly a religious or heritage site."\
    },\
    {\
      "question": "Based on the clothing of the individuals, what is the likely weather in the image?",\
      "answer": "The weather appears to be cool or mild, as most individuals are wearing long sleeves and pants."\
    },\
    {\
      "question": "What can be inferred about the popularity of the location?",\
      "answer": "The location seems to be popular, as there are several groups of people visiting, indicating it might be a tourist attraction or a place of interest."\
    },\
    {\
      "question": "Considering the design of the buildings, what region or culture might it represent?",\
      "answer": "The blue tiles and domed structures suggest that the architecture may be of Islamic influence, likely representing Middle Eastern or Central Asian culture."\
    },\
    {\
      "question": "How do the individuals in the image appear to be engaged with the location?",\
      "answer": "The individuals are walking and observing their surroundings, implying they are visitors or tourists exploring the site."\
    },\
    {\
      "question": "Judging by the path and layout, what is the likely purpose of this corridor?",\
      "answer": "The corridor likely serves as a pedestrian walkway guiding visitors between different sections of the historic or cultural site."\
    },\
    {\
      "question": "What time of day does it appear to be in the image?",\
      "answer": "Given the natural light and shadows, it seems to be daytime, possibly late morning or early afternoon."\
    }\
  ],\
  [\
    {\
      "question": "What does the scenery around the individual suggest about the location?",\
      "answer": "The lush greenery, rice fields, and mountain in the background suggest a rural, tropical environment, possibly in Southeast Asia."\
    },\
    {\
      "question": "What activity is the person in the image most likely doing?",\
      "answer": "The person seems to be walking down a path, likely hiking or exploring the rural landscape."\
    },\
    {\
      "question": "Considering the walking path, what is its likely purpose in this setting?",\
      "answer": "The walking path is most likely intended for touring or exploring the rice fields and the surrounding natural landscape."\
    },\
    {\
      "question": "Based on the image, what can be deduced about the time of year?",\
      "answer": "The verdant fields and clear weather suggest it might be during a growing season and not the dry or cold season."\
    },\
    {\
      "question": "How does the attire of the person suggest preparedness for the setting?",\
      "answer": "The person\'s attire including a backpack and comfortable clothing indicates they are prepared for outdoor activities like hiking or walking."\
    },\
    {\
      "question": "What might be the benefit of the walkway\'s design in this environment?",\
      "answer": "The raised brick walkway helps visitors traverse the area without disturbing the rice fields and protects them from wet ground."\
    },\
    {\
      "question": "What can be said about the weather at the moment in the photograph?",\
      "answer": "The weather seems fair with a mix of sun and clouds, ideal for outdoor activities like walking or hiking."\
    }\
  ]\
]\
```'
        self.mock_openai.chat.completions.create.return_value = self.mock_response

        self.diction = {'image_subset/images/sa_234937.jpg': [{'question': 'What might be the cultural significance of the place where the people are walking?', 'answer': 'The intricate tile work and the architectural design suggest that it is a place of historical or cultural significance, possibly a religious or heritage site.'}, \
                        {'question': 'Based on the clothing of the individuals, what is the likely weather in the image?', 'answer': 'The weather appears to be cool or mild, as most individuals are wearing long sleeves and pants.'}, \
                        {'question': 'What can be inferred about the popularity of the location?', 'answer': 'The location seems to be popular, as there are several groups of people visiting, indicating it might be a tourist attraction or a place of interest.'}, \
                        {'question': 'Considering the design of the buildings, what region or culture might it represent?', 'answer': 'The blue tiles and domed structures suggest that the architecture may be of Islamic influence, likely representing Middle Eastern or Central Asian culture.'}, \
                        {'question': 'How do the individuals in the image appear to be engaged with the location?', 'answer': 'The individuals are walking and observing their surroundings, implying they are visitors or tourists exploring the site.'}, \
                        {'question': 'Judging by the path and layout, what is the likely purpose of this corridor?', 'answer': 'The corridor likely serves as a pedestrian walkway guiding visitors between different sections of the historic or cultural site.'}, \
                        {'question': 'What time of day does it appear to be in the image?', 'answer': 'Given the natural light and shadows, it seems to be daytime, possibly late morning or early afternoon.'}], 'image_subset/images/sa_234938.jpg': [{'question': 'What does the scenery around the individual suggest about the location?', 'answer': 'The lush greenery, rice fields, and mountain in the background suggest a rural, tropical environment, possibly in Southeast Asia.'}, \
                        {'question': 'What activity is the person in the image most likely doing?', 'answer': 'The person seems to be walking down a path, likely hiking or exploring the rural landscape.'}, {'question': 'Considering the walking path, what is its likely purpose in this setting?', 'answer': 'The walking path is most likely intended for touring or exploring the rice fields and the surrounding natural landscape.'}, \
                        {'question': 'Based on the image, what can be deduced about the time of year?', 'answer': 'The verdant fields and clear weather suggest it might be during a growing season and not the dry or cold season.'}, {'question': 'How does the attire of the person suggest preparedness for the setting?', 'answer': "The person's attire including a backpack and comfortable clothing indicates they are prepared for outdoor activities like hiking or walking."}, \
                        {'question': "What might be the benefit of the walkway's design in this environment?", 'answer': 'The raised brick walkway helps visitors traverse the area without disturbing the rice fields and protects them from wet ground.'}, {'question': 'What can be said about the weather at the moment in the photograph?', 'answer': 'The weather seems fair with a mix of sun and clouds, ideal for outdoor activities like walking or hiking.'}]}
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the temporary directory after testing
        shutil.rmtree(self.test_dir)

    def test_run_image_batch(self):
        with patch('run_batch.get_gpt_response', return_value=self.mock_response.choices[0].message.content):
            image_batches = [['image_subset/images/sa_234937.jpg', 'image_subset/images/sa_234938.jpg']]
            ipath2qa_pairs = run_image_batch(0, self.mock_openai, 'test_prompt', image_batches, 'output.json', 'debug', 'batch.json')
            self.assertEqual(ipath2qa_pairs, self.diction)

    def test_run_batch_safe(self):
        with patch('run_batch.run_image_batch', side_effect=Exception('Test Exception')):
            result = run_batch_safe(0, self.mock_openai, 'test_prompt', {'batch': ['image.jpg']}, 'output.json', 'debug', 'batch.json')
            self.assertEqual(result, {})

    def test_run(self):
        with patch('run_batch.run_batch_safe', return_value={'image.jpg': ['answer1', 'answer2']}):
            ipath2qa_pairs = run({'batch': ['image.jpg']}, self.mock_openai, 'test_prompt', 'output.json', 'debug', 'batch.json')
            self.assertEqual(ipath2qa_pairs, {'image.jpg': ['answer1', 'answer2']})

    def test_save_batch(self):
        with patch('builtins.open', mock_open()) as mock_file:
            output_path = os.path.join(self.test_dir, 'output.json')
            save_batch('test_prompt', {'image.jpg': ['answer1', 'answer2']}, output_path)

            # Assert that 'open' was called with the correct arguments
            mock_file.assert_called_once_with(output_path, 'w')
            
            # Get the handle to the opened file
            handle = mock_file()
            
            # Assert that 'write' was called with the expected JSON content
            handle.write.assert_called_once_with(json.dumps({
                'prompt': 'test_prompt',
                'data': {'image.jpg': ['answer1', 'answer2']}
            }, indent=4))

class TestConsolidateAnswers(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the temporary directory after testing
        shutil.rmtree(self.test_dir)

    def test_consolidate_and_save(self):
        # Mocking command line arguments
        with patch('sys.argv', ['consolidate_answers.py', '--answers_dir', self.test_dir]):
            # Creating dummy batch files
            dummy_data = [{"prompt": "TestPrompt", "data": { "test1.jpg": [{"question": "q1", "answer": "a1"}, {"question": "q2", "answer": "a2"}]}},\
            {"prompt": "TestPrompt", "data": { "test2.jpg": [{"question": "q3", "answer": "a3"}, {"question": "q4", "answer": "a4"}]}}]
            for i in range(2):
                with open(f'{self.test_dir}/batch{i}.json', 'w') as f:
                    json.dump(dummy_data[i], f)

            # Run consolidation
            args = parse_arguments()
            prompt, combined_data = consolidate(args)

            # Ensure the prompt and combined_data are correct
            print(combined_data)
            self.assertEqual(prompt, 'TestPrompt')
            self.assertEqual(combined_data, {'test1.jpg': [{'question': 'q1', 'answer': 'a1'}, {'question': 'q2', 'answer': 'a2'}], 
                                             'test2.jpg': [{'question': 'q3', 'answer': 'a3'}, {'question': 'q4', 'answer': 'a4'}]})

            # Save consolidated data to a temporary file
            output_file = f'{self.test_dir}/test_output.json'
            args.output_fpath = output_file
            save_consolidated(args, prompt, combined_data)

            # Check if the output file exists
            self.assertTrue(os.path.exists(output_file))

            # Load the saved data and check if it matches the original data
            with open(output_file, 'r') as f:
                saved_data = json.load(f)

            self.assertEqual(saved_data['prompt'], prompt)
            self.assertEqual(saved_data['data'], combined_data)

if __name__ == '__main__':
    unittest.main()
