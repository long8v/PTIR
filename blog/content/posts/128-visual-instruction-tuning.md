---
title: "Visual Instruction Tuning"
date: 2023-06-09
tags: ['multimodal', 'NeurIPS', '2023Q2']
paper: "https://arxiv.org/abs/2304.08485"
issue: 128
issueUrl: "https://github.com/long8v/PTIR/issues/128"
summary: "to read llava 1.5 - probably the first work that created instruction data to assist. open sourced well and is widely used"
---
<img width="594" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/534c85ad-90d1-40e2-9097-ed2d205e1170">


[paper](https://arxiv.org/abs/2304.08485)

## TL;DR
- **I read this because.. :** to read llava 1.5
- **task :** chatting VLM
- **problem :** Let's make instruction-following work for multi-modal like chatGPT
- **idea :** put bbox and caption in language only GPT and have it create QA
- **input/output :** image + Q -> A
- **architecture :** LLaMA 13B + CLIP + projection
- **objective :** ce loss 
- **baseline :** GPT-4, BLIP-2, OpenFlamingo
- **data :** (feature alignment) filtered during CC3M (e2e learning) instruction data or SicenceQA created with GPT4 or chatGPT with captions and bboxes for COCO images
- **evaluation :** Create a question sampling from coco and ask GPT-4 to re-evaluate the answer that GPT-4 came up with when asked the question with bbox and caption.
- **result :** Good performance on scientific QA, good at higher-level reasoning (such as humor interpretation) that BLIP-2 / OpenFlamingo / GPT-4 are not good at
- **contribution :** Probably the first work to create instruct data to assist. open sourced well and widely used
- **etc. :**

## Details
### Instruction following data 
- Create a caption and bbox for a COCO image
- converstaion(58K) / detailed description(23K) / complex reasoning(77K)
<img width="500" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/6b096002-2370-4f65-8538-06f25683523a">

<img width="500" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5dd53143-8c24-4400-b2ab-048d3231b9bd">

Ablation for this.
Adding detailed captions improves performance on the chatbot side. It seems to help with reasoning.

### Training 
input sequence

<img width="696" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/de4a7e3e-1884-48bb-83f1-02818648b5e0">

<img width="641" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/8f9d6b64-b5eb-4295-9930-274a20a7e974">

The first question can be an image first or a question first, and the order is randomized by using the

<img width="448" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ad5a59e1-8bad-4081-b467-9e10d8b4bba9">

<img width="867" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/7ff9dafe-f9ca-4b53-9072-d8cc3909be8f">


- pre-training feature alignment
Filtering only 595K image text on CC3M + learning only linear projection
Use the caption as is, but format it as a simple instruction following (single turn, ask to briefly describe the image)
In this case, the filtering method is as follows (uniformly fit by noun frequency)

<img width="705" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/eb673bd0-9954-480d-ac20-ed84b1283d3b">

<img width="678" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4028fd16-6ad9-44a0-a5ba-191a09feade4">

- finetuning end-to-end
Freeze only the vision encoder and learn the rest of projection + LM

### Ability 
<img width="1500" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/1e600282-57ab-464f-9c7b-b93e88408dec">

I'm wondering how to make it for complex reasoning, but it says to put [system prompt](https://github.com/haotian-liu/LLaVA/blob/main/playground/data/prompts/complex_reasoning/system_message.txt) like this
```
You are an AI visual assistant that can analyze a single image. You receive five sentences, each describing the same image you are observing. In addition, specific object locations within the image are given, along with detailed coordinates. These coordinates are in the form of bounding boxes, represented as (x1, y1, x2, y2) with floating numbers ranging from 0 to 1. These values correspond to the top left x, top left y, bottom right x, and bottom right y.

The task is to use the provided caption and bounding box information, create a plausible question about the image, and provide the answer in detail.

Create complex questions beyond describing the scene.
To answer such questions, one should require first understanding the visual content, then based on the background knowledge or reasoning, either explain why the things are happening that way, or provide guides and help to user's request.  Make the question challenging by not including the visual content details in the question so that the user needs to reason about that first.

Instead of directly mentioning the bounding box coordinates, utilize this data to explain the scene using natural language. Include details like object counts, position of the objects, relative position between the objects.  

When using the information from the caption and coordinates, directly explain the scene, and do not mention that the information source is the caption or the bounding box.  Always answer as if you are directly looking at the image.
```

### Ablations 
<img width="343" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/2475db52-a066-45b0-976f-a5c540ee46e7">

- ViT last layer vs previous layer -> previous layer is better
- Applying CoT i.e. answer then reasoning / Reasoning then answer -> convergence was faster for reasoning - answer, but not final performance
- Skip the alignment learning step and go straight to learning -> worse performance
- LLM 13B to 7B -> Worse Performance


### Play with demo 
https://llava.hliu.cc/
Playing with the demo
<img width="960" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/431de7ba-f0fb-4d4b-a975-256cbb154bda">

Good at general explanations

I tried to generate a scene graph.
<img width="971" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/7d755617-be67-441d-9fea-89889657586f">

<img width="972" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/fc82b08f-4ddc-4494-b74b-e21eb02a9493">

<img width="981" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ccd16297-657b-4625-b6af-cb93551ffeee">

Predicate is no longer a verb...
<img width="984" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/7803f163-bbf8-4db4-b1c2-2f5ac454469e">

Start lying...

If you give a bad example, just include it in your answer. You're still making a triplet that makes sense.
<img width="959" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/1ae11635-62cd-400e-93a6-8b63f007bd17">

<img width="932" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/f06bd7d4-18fa-4177-84d5-e28c7811f10d">

Here we have hallucination... visual genome was probably in the training data, so let's get some other data.
This photo I took in Taiwan...

<img width="490" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b4bf4bf5-fe6b-4c2c-ad68-81ecf107df2e">

<img width="951" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/7bde0a9b-8376-4a76-b8bb-294f00991332">

I don't know where child is, but I'm guessing it's

<img width="975" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d5a72445-4aeb-4742-8bdb-461d44b7491f">

<img width="300" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d775d09b-4f96-4d2d-b9ce-dd0cae1f6097">

It's a pretty clear sample

<img width="980" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d36c4342-071f-47b2-a6f2-efeee2a4ad88">

It's starting to get good lol

<img width="965" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b2e1b227-7cfd-4ee1-9d25-a4350eab306d">

I changed the prompt and suddenly it started saying the right thing again...

It works well because it gives a good example, but where's the baby?
<img width="958" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/26035797-a5dc-49b7-8e3a-db317f950df7">

I post a picture of my kid from Busan, which is very relatable lol and wouldn't be weird to have in a benchmark.
<img width="300" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/34a009b5-799e-4249-b37f-b17a839880a6">


<img width="954" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/27d3b6cb-90bb-4d0e-8d86-9cebc6cd468c">

Perfect.
<img width="973" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/98e7557c-e455-4c50-8081-7b6ca7aa32f1">

It's a bit of a homophone, but you're not wrong.

<img width="956" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/43308a72-acf5-4df8-9fdc-b8d0d5f6d650">

On an emotional note...

<img width="979" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ea9670aa-4d69-42bf-8ff3-7a039f63b5f4">
<img width="967" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d966a85b-a618-4fc7-9b7a-f3cf361310da">

Section 3 Section 4 Good at taking a knock...
