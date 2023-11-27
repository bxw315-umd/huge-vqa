# Huge VQA Dataset

## Image Dataset
We have decided to use the [Segment Anything dataset](https://segment-anything.com/dataset/index.html)
created by Meta AI. For prompt engineering, testing, and evaluation we chose 110 images, which
can be found [here](./image_subset). The 10 pictures in the prompt engineering folder were
ones that we found to be interesting or challenging for models to perceive.

The generic tool we build will be able to take in any folder of image files to generate
Q/A pairs.

## Captioning
Because pre-captioned image datasets such as [COCO](https://cocodataset.org/#home) are smaller than
desired and other large datasets such as [LAION](https://laion.ai/projects/) aren't of the same
quality we desire, we have included an image-to-caption process in our tool. To do this,
we will use the top two state of the art models to generate two detailed captions.
The two top VQA/Captioning models are [Llava1.5](https://llava-vl.github.io/) and
[InstructBLIP](https://arxiv.org/abs/2305.06500).

### Prompt-Engineering
Current Prompt: *"Offer a thorough analysis of the image"*

## Usage
1. Generate question batches from a root image folder

```python scripts/generate_batches.py --image_folder images --batch_size 80```

This will output question batches as json files in export/question_batches

2. Run a question batch

```python scripts/run_batch.py --batch_fpath export/question_batches/batch_2_of_3.json --output_fpath export/answer_batches/batch_2_of_3.json --prompt_fpath prompts/current.txt --debug_dir export/debug```

This will output parsed GPT Q/A pairs in export/answer_batches/batch_2_of_3.json

3. Consolidate batch outputs into one file

```python scripts/consolidate_answers.py --answers_dir export/answer_batches --output_fpath export/answers.json```

4. Visualize Q/A pairs

```flask --app visualization/app.py run --debug```