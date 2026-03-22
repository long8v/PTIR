---
title: "[137] mPLUG-Owl2: Revolutionizing Multi-modal Large Language Model with Modality Collaboration"
date: 2023-12-05
tags: ['multimodal', 'LLM', '2023Q4', 'alibaba']
paper: "https://arxiv.org/abs/2311.04257"
issue: 149
issueUrl: "https://github.com/long8v/PTIR/issues/149"
summary: "very recent VLM model - Is this the first time a VLM model also improves text performance?"
---

<img width="813" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/679dc334-d193-439c-b819-66b32c4fb322">

[paper](https://arxiv.org/abs/2311.04257)

## TL;DR
- **I read this because.. :** very recent VLM model
- **task :** VLM + LLM
- **problem :** multi-modal task freezes LLM and actually tries to do V+L well, but I want both V/L to do well.
- **idea :** Overall BLIP-2 style, with the difference that the LLM has different $W_K$, $W_V$, and Norm for each modality, and the LLM is tuned accordingly.
- **input/output :** text + image -> text 
- **architecture :** CLIP ViT-L/14 + vision abstractor(=Q-former) + LLaMA-2 w/ Modality-Adaptive Module(MAM)
- **objective :** ce loss
- **baseline :** Models based on the 7B LLM. BLIP-2, MiniGPT-4, LLAVA, mPLUG-Owl, InstructBLIP, Otter, Qwen-VL-Chat, LLaVA-1.5
- **data :** 400M samples from {CC3/12M, COCO, COYO, LAION-en, DataComp} for pretraining / {captioning(TextCaps, COCO), VQA(VQAv2, OKVQA, OCR-VQA, GQA, A-OKVQA), region-aware(RefCOCO, VisualGenome), multi-modal instruction(LLaVa-instruct-150k), text-only instruction data(ShareGPT80-K, SlimOrca)}
- **evaluation :** caption / vqa / multimodal benchmark(MME, MMBench, MM-Vet, SEED-Bench, Q-Bench) / text benchmark(MMLU, BBH, AGIEval, ARC-c, ARC-e)
- **Result :** Almost all of the 7B models are sota. textual instructions are also used + MAM improves performance over LLaMA2 even in pure text benchmarks.
- **contribution :** VLM model also improves text performance?
- **etc. :** alibaba money is good....

## Details
<img width="493" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/efad2f51-3e9c-4bc7-a499-ebe1edcae6dd">

### Architecture
<img width="973" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/1b1bc124-7120-4799-a689-47c21ad6a81c">

- Vision Abstractor eventually uses the Q-former
- Modality-Adaptive Module will eventually have a different weight/norm depending on the modality of the input. But the query weight is the same. Here, W for images is newly initialized, so it is learned in step-1 pretraining.
- There are two learning phases
1) For pre-training, use these {CC3/12M, COCO, COYO, LAION-en, DataComp} to learn the initialized parts of the vision encoder / q-former / language decoder.
It would be interesting to compare it to [BLIP-2](https://docs.google.com/presentation/d/1SBMWFARCLolhcGyKCT7-TzPt1l7hDkMByiT9TWZfOqM/edit#slide=id.g245ab93dc34_1_26), where BLIP-2 takes CLIP ViT and freezes the vision encoder. And the images it uses are newly captured data (CapFilt) from a similar source.
Here, we don't freeze the vision encoder and just use the relatively noisy alt-text! In a way, we're retraining the kind of data we saw in CLIP in a generative form.
2) In joint-instruction tuning, we unfreeze everything and learn only with instruction data. The difference is that we also added text instruction data.

<img width="517" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/50bf1220-295d-4388-98e9-ec39268a584a">

The difference between the two steps is resolution / LLM seq len

### Result
- caption, VQA / multi-modal benchmark
<img width="982" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/7fe4a521-f562-4206-8e7b-08970c73747c">

- pure text benchmark
<img width="486" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/c7ceb420-d999-4005-88af-dcfa7d75c9e7">

Saying it's because of MAM
<img width="462" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/7e40d6e4-7956-4738-9804-a2dd787851f4">

- Effect of using two modalities for instruction data + effect of MAM
 
<img width="478" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ce00bdb1-3c42-4eac-8fd4-669357337ca8">

Using text intstruction data makes mm perform worse, using mm instruction makes text worse, using both makes both perform slightly worse than either alone + using MAM makes both better

- vision encoder freeze effect
<img width="472" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/994fb00a-18d7-4294-ae18-d9fe5bbabc9d">

- num queries
<img width="480" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ef6c5b45-702d-4825-ac03-79c10c36ca87">

Requires a lot of text VQA

- resolution
<img width="460" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/0966b184-7425-4af1-a621-8b5c19820ab7">

textVQA works overwhelmingly well lol

### Qualitative Result
<img width="471" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5db5f102-c6ea-40e4-808b-3ab54905e040">

Claims to see text in early layers and images in later layers thanks to MAM -> what's the point?

<img width="498" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/f5e9124f-3add-44e3-8c81-64322ee27e20">

Given an unrelated image and text, state that you focused on the text if you have a MAM
I think you're both wrong, but if you have a MAM, you'll say at least 7 lol