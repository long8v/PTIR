---
title: "MiMo-VL Technical Report"
date: 2025-07-02
tags: ['MLLM', 'reasoning', '2025Q2']
paper: "https://arxiv.org/abs/2506.03569"
issue: 233
issueUrl: "https://github.com/long8v/PTIR/issues/233"
summary: "LVLM2 reporting AIME - beats other models in most benchmarks, highest Elo in open source"
---
<img width="665" alt="Image" src="https://github.com/user-attachments/assets/1a8adacd-f766-4054-aeae-ef996201fc43" />

[paper](https://arxiv.org/abs/2506.03569), [code](https://github.com/XiaomiMiMo/MiMo-VL)

## TL;DR

* **I read this because.. :** LVLM2 reporting AIME
* **task :** multimodal understanding, reasoning, GUI grounding
* **PROBLEM :** A model that is good at both reasoning and understanding.
* **idea :** massive pretrain + rl
* **input/output :** {(image, video), prompt}→ answer or action
* **architecture :** Qwen2.5-ViT + MLP projector + MiMo-7B
* **objective :** CE loss(pretrain, SFT), on-policy GRPO(RL)
* **baseline :** Qwen2.5-VL, InternVL3, GPT-4o, UI-TARS, etc.
* **data :** 2.4T token for pretraining(caption, interleaved, ocr, grounding, gui, synthetic reasoning) 
* **evaluation :** 50+ benchmarks (MMMU, OlympiadBench, GUI, etc.)
* **result :** Outperforms other models in most benchmarks, highest Elo in open source
* **contribution :** 
* **etc. :** Raises intertask interference issues, can handle long-context


## Details
### architecture 

<img width="848" alt="Image" src="https://github.com/user-attachments/assets/b874b1ca-7d69-4ba1-acd7-528a1138ddaf" />

- strong reasoning abilities inherent in MiMo-7B-Base (Xiaomi, 2025), enabling their seamless transfer and adaptation to multimodal contexts. Consequently, this allows our model to exhibit powerful and versatile multimodal reasoning capabilities across a broad array of domains. -> Already MIMO based but seems to have Reasoning ability.

### training

<img width="631" alt="Image" src="https://github.com/user-attachments/assets/ba557164-96b9-4353-9243-387b19930d47" />

Raise to 32K in stage 4

#### pre-training
Learn 2.4T token
- implement dedicated data curation pipelines tailored to the characteristics of each data type
- data
  - Image Caption Data : dedup (image perceptual hashing), text filtering, re-caption(w/ linguistic consistency, repititon filtering, imbalance filtering (w/ MetaCLIP)
  - interleaved data: webpages, books, academic papers, pdf parsing, knowledge density and readability filtering, ...
  - ocr : to increase learning difficulty, handwritten, typographically deformed, blury occluded, bounding box annotated
  - grounding data: single / multiple objects
  - video: publicly available, video recaptioning, dense finegrained, event distribution, challenging question about video and synthesize response
  - GUI data : open source & synthetic. grounding, action
- synthetic reasoning : image, prompt are collected as open source and MiMo-7B-base is used for generation. Strict filtering to evaluate not only the correctness of the answer but also the clarity of thought, remove redundancy, and ensure consistent formatting.

#### post-training 
![Image](https://github.com/user-attachments/assets/29c59096-912d-4b30-b5fe-4ce697532a8f)
 
- RLVR
  - data
    - visual reasoning: open source & k-12 collection
      - LLM is prompted to filter proof-based problems and rewrite multiple-choice questions with numerical or symbolic answers into free-answer formats, alleviating potential reward hacking
    - text reasoning : include more challenging queries requiring college or competition-level intelligence (than visual reasoning, K12)
- Image Grounding: Whether the GIoU or point is inside the box.
    - Temporal Video Grounding : video moment retrieval [mm:ss,mm:ss] -- IoU
- RLHF
- mixed on-policy RL
- RLVR + RLHF combined to learn with GRPO
- The difference with GRPO is that it is completely on-policy (reloading vllm every time), so there is no clipping or importance sampling part
    -  <img width="449" alt="Image" src="https://github.com/user-attachments/assets/1004a22b-54b7-4600-bd0d-f6a0319b5c0a" />
    - <img width="308" alt="Image" src="https://github.com/user-attachments/assets/6751ba2f-d54a-4313-a095-643814ff7fb4" />
    - c.f. GRPO
     -  <img width="1271" alt="Image" src="https://github.com/user-attachments/assets/0a1ae91c-fc5d-47b1-ba4d-ed7f6c3f717c" />


### performance

<img width="623" alt="Image" src="https://github.com/user-attachments/assets/19b8677b-0ad2-4c6e-9572-97a8ef3e3d3c" />

Not much fun in the RL phase

<img width="643" alt="Image" src="https://github.com/user-attachments/assets/7a131113-5afc-42d2-bc78-687942b93a89" />



### ablation

<img width="670" alt="Image" src="https://github.com/user-attachments/assets/eda60ef1-0c93-4d1f-839a-20212eac7d7b" />

Is it because there is no KL term?

<img width="627" alt="Image" src="https://github.com/user-attachments/assets/ae025ed5-2c48-41fd-9ea9-3af828bb6d5c" />

### challenges 
- Interference Between RL Tasks: grounding task like grounding trajectory is not long and reasoning is long, so it was difficult to get as much performance as RL doing each because they move in opposite directions.

<img width="793" alt="Image" src="https://github.com/user-attachments/assets/8ca058fd-3936-41e8-984c-46cdb41a2a97" />

aime24 68.0 to 80.1 (max len 48K) with mimo 7B-rl https://huggingface.co/XiaomiMiMo/MiMo-7B-RL

(67 points in this paper)