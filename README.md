# Huge VQA Dataset Tool

This repository contains a tool for generating a huge visual question-answering (VQA) dataset. It does so by
using GPT-4V(ision) to automatically generate question-answer pairs for given images. This allows the tool
to generate a dataset larger than existing datasets, which all require some level of crowdsourcing.
Includes:
- Tool to go from downloaded images -> JSON with question-answer pairs for each question
- Visualization tool to create human-readable results
- A demo/starter dataset hosted on [Google Drive] *link here*

## Installation and Setup

### Installation
1. Clone this repository.
2. In your chosen environment, install dependencies using `requirements.txt`.

### OpenAI Setup
In order to use the tool, you must have the OpenAI API set up. You can set up your account [here](https://openai.com/blog/openai-api).

**IMPORTANT**: Set up your API key following [the instructions here at Step 2](https://platform.openai.com/docs/quickstart?context=python).

## Usage
Use these commands from the root folder of the repository to run the tool.

1. Generate question batches from a root image folder

```python scripts/generate_batches.py --image_folder images --batch_size 80```

This will output question batches as json files in export/question_batches

2. Run a question batch

```python scripts/run_batch.py --batch_fpath export/question_batches/batch_2_of_3.json --output_fpath export/answer_batches/batch_2_of_3.json --prompt_fpath prompts/current.txt --debug_dir export/debug```

This will output parsed GPT Q/A pairs in export/answer_batches/batch_2_of_3.json

3. Consolidate batch outputs into one file

```python scripts/consolidate_answers.py --answers_dir export/answer_batches --output_fpath export/answers.json```

4. Visualize Q/A pairs

```flask --app visualization/app.py run --debug``` needs fixing

## Image Dataset
We have decided to use the [Segment Anything dataset](https://segment-anything.com/dataset/index.html)
created by Meta AI. For prompt engineering, testing, and evaluation we chose 110 images, which
can be found [here](./image_subset). The 10 pictures in the prompt engineering folder were
ones that we found to be interesting or challenging for models to perceive.

Our demo/starter dataset can be found at [this google drive] *Need Link*. *Talk about dataset briefly

*In order to use the results from the dataset you will need to download the first 2 tar files [here](https://scontent-iad3-2.xx.fbcdn.net/m1/v/t6/An8MNcSV8eixKBYJ2kyw6sfPh-J9U4tH2BV7uPzibNa0pu4uHi6fyXdlbADVO4nfvsWpTwR8B0usCARHTz33cBQNrC0kWZsD1MbBWjw.txt?ccb=10-5&oh=00_AfDnBt9Rekikl1latWWVAvKIVv8JbNoXcY__FqIcWaYbTQ&oe=65A314D8&_nc_sid=0fdd51).

The generic tool we build will be able to take in any folder of image files to generate
Q/A pairs.

## Examples
