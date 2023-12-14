import unittest
import tempfile
import shutil
import os
import argparse
from generate_batches import generate_batches, save_batches, parse_arguments

class TestImageBatchGeneration(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the temporary directory after testing
        shutil.rmtree(self.test_dir)

    def test_full_process(self):
        # Create some dummy image files for testing
        dummy_image_paths = [os.path.join(self.test_dir, f'image_{i}.jpg') for i in range(1, 10)]
        for path in dummy_image_paths:
            with open(path, 'w') as f:
                f.write("Dummy image content")

        # Create a dummy argument namespace
        dummy_args = argparse.Namespace(
            image_folder=self.test_dir,
            batch_size=1  # Set a small batch size for testing
        )

        # Call the main processing functions
        batches = generate_batches(dummy_args.image_folder, int(dummy_args.batch_size))
        save_batches(batches, root_path=self.test_dir)

        # Verify the generated batches
        self.assertEqual(len(batches), 2)  # Adjust this based on your specific test case

        # Verify the saved batches
        for i in range(len(batches)):
            batch_path = os.path.join(self.test_dir, f'batch_{i+1}_of_{len(batches)}.json')
            self.assertTrue(os.path.exists(batch_path))

if __name__ == '__main__':
    unittest.main()
