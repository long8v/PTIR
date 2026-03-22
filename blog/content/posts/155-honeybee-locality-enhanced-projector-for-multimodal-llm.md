---
title: "[143] Honeybee: Locality-enhanced Projector for Multimodal LLM"
date: 2023-12-22
tags: ['kakao', '2023Q4', 'MLLM']
paper: "https://arxiv.org/pdf/2312.06742.pdf"
issue: 155
issueUrl: "https://github.com/long8v/PTIR/issues/155"
summary: "Read about ablation for data recipe because you did a good job - identify and improve weaknesses in resampler. Sharing tips on various recipes (Hye-Ja paper..)"
---
<img width="788" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5174178f-8ae5-47f4-9d3c-5ea8ffec9fa7">

[paper](https://arxiv.org/pdf/2312.06742.pdf)

## TL;DR
- **I read this because.. :** I read this because you did a good job of ablation for the data recipe
- **task :** MLLM 
- **problem :** projector has the effect of lengthening the seq len, and the resampler structure is not locally-aware, which seems to hurt the score.
- **idea :** use conv or deformable attention instead of linear projection
- **input/output :** image, text(query) -> text(answer)
- **architecture :** CLIP ViT-L/14 + ResNet or DDETR (with minor changes) + LLM (Vicuna-7B / 13B)
- **objective :** LM loss
- **baseline :** LLaVA, MiniGPT-4, LLaMA-Adatper2, mPLUG-owl, InstructBLIP, IDEFICS, Shikra, Qwen-VL, LLaVA-1.5
- **data :** (pretraining) COYO100M, BLIP-CapFilt (instruction) captioning(BlipCapFilt, COYO100M), VQA-open(VQAv2, GQA, OCRVQA, VSR), VQA-mc(SicenceQA, A-OKVQA), REC(RefCOCO, RefCOCO+, RefCOCOg, VG), Instruction(LLaVA150K, ShareGPT)
- **evaluation :** SEED(limb), MME, MMB(binary), LLAVAW
- **result :** sota
- **contribution :** Identified and improved weaknesses in the resampler. Shared tips on various recipes (Hyeja's paper..)
- **etc. :** 준범님 참여한 논문 다 좋은듯.

## Details
- motivation 
<img width="547" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/c6452755-e41c-4b97-982a-2204d1c5a266">

Analyzing spatial-related challenges in benchmarks linear projection vs resampler
Analysis that resampler kids are bad at spatial. Finer details are lost in the sampler process.
Linear styles, on the other hand, tend to convey local information well

### Honey-bee
<img width="1015" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/88d988cc-17ea-4ac0-a3e6-a5cfcc67dc8f">

 - MLLM objective

 <img width="477" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a8d542ba-b34f-41da-9a58-f741d58827a2">

- architecture

1) vision encoder 2) projector 3) large language model

- efficieny of mllm
Most of the bottlenecks (memory consumption, throughput) are in the LLM, meaning that the number of visual tokens you pass to the LLM determines its efficiency.

<img width="496" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/45911fd4-5250-409f-a94a-06481c31c3f3">

<img width="510" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/0ab1f1c0-5177-4617-ba98-e7583871ee09">

For example, linear projection has very few parameters, but has a similar time to the same # tokens resampler. In other words, training time is proportional to # tokens.
How resampler takes longer to learn a step as the #visual token increases
(A slightly different point from llava's claim that it converges quickly with fewer parameters. There we say "converge" because of the fewer parameters, here we just mean the speed of learning right away)

- proposed

As mentioned in the motivation, it seems that the resampler structure doesn't reflect locality. Let's add a visual projector to reflect locality.

- Abstractor 
<img width="460" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/44d70363-a302-4ad2-807e-7715315cae50">

C-abstractor is a ResNet
The D-abstractor is a Deformable Attention

Result
<img width="500" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4f87d6d5-eb0e-4f66-ac30-3cd8447049e8">


### Training 
Overall, the llava-like training strategy
- Pre-training for vision-language alignment.
1:1 COYO to BlipCapFilt (this ratio was determined after a short manual learning curve)
Learn projector only

- visual instruction tuning
Learn like an LLM with projector
The data looks like this
<img width="485" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/8fdac703-b5af-46b3-ab80-6db9964a4032">

<img width="427" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/847204f8-a910-4a03-9333-15c4e804076b">


###  Hidden Recipe for Visual Instruction Tuning
<img width="638" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/dc7c4fd2-9186-46eb-ad14-374f632cf464">

- Dataset Combination
- It's good to have a variety of
- Benchmark performance drops significantly, especially when open-ended VQAs are removed
- MMB, SEED drops a lot when multiple-choice VQAs are removed -> important for aligning response patterns
- LLAVAW drops significantly when captioning data is removed -> LLAVAW favors narrative and descriptive responses
- LLaVAW (evaluating to GPT) drops when using visual or text instruction-following datasets.

<img width="369" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/48cc0512-9977-442f-bd30-d9fd651b6417">

- Dataset Balancing
- When pretraing, the 1:1
- instruction, you can only tune it manually ㅜㅜ
<img width="450" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/2fb50411-fec2-4a80-a4f8-0916094180a4">

VSR, ShareGPT, ScienceQA, and OCRVQA have lower absolute amounts, reducing the ratio
OCRVQA, VG reduced experimentally
I left out BlipCapFilt for captioning because of cost, but ablation didn't degrade performance (!! you took alt-text and threw away caption)
 
- Instruction vs Multi-task
<img width="416" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/3218e109-ff32-4e86-993f-3bb27d105989">

Instruction is better when given as an instruction vs. dataset or task name

- template

<img width="415" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/db38de3b-e178-43e4-8986-2c8319fc7a64">

For granularity, it was nice to have different templates per "task" (!!)
It was better to use one template than multiple (!!)
flip reverses the order of QA, but it's not very helpful

- multi-turn
<img width="414" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/246eca15-8ff9-4060-bbf4-343217bc596e">

It was nice to have multi-turn VQA, especially since it deduplicates similar questions.
<img width="860" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5f9b242d-b04d-43e0-b8af-c2b8d911be4f">


- Evaluation
<img width="382" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/39349ad4-8ace-4789-8c6c-4f64b9356027">


### D-etails
- examples of benchmarks
<img width="466" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/fb5f984d-3990-461a-b1fd-7827911e79cc">


SEED says a lot of fine-grained

- Designing the architecture of the resampler
<img width="336" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/28905c98-33a9-4dbd-bd05-6c0f0faad81b">

- Templates
<img width="686" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/2d137ca3-bd87-481b-a18b-65369045304e">

Captions can be added to the
Change VQA, REC tasks to fine-grained
For example, in [Visual Semantic Reasoning] (https://paperswithcode.com/dataset/vsr), replace The cat is inside the refrigerator, False with Is the cat inside the refrigerator?
And use what's already there for instruction without template
