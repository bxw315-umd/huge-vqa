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
