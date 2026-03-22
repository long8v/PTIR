---
title: "Qwen3-VL Technical Report"
date: 2026-03-09
tags: ['MLLM', 'qwen', '2025Q4']
paper: ""
issue: 243
issueUrl: "https://github.com/long8v/PTIR/issues/243"
---
<img width="831" height="278" alt="Image" src="https://github.com/user-attachments/assets/e6eb3007-9c0f-4290-be48-0c1b768ac14e" />

[paper]( )

## TL;DR
- **I read this because.. :** It's old, but it seems to be volatilizing, so I organized it.
- **task :** MLLM 
- **IDEA :** square-root reweighting for arch variation, balance by modality
- **input/output :** {text, image, video} -> text
- **architecture :** interleaved-MRoPE, DeepStack, textual timestamp for video temporal grounding / Dense(2B, 4B, 8B, 32B), MoE(30B-A3B, 235B-A22B)
- **objective :** CE loss -> GSPO 
- **baseline :** Gemini 2.5 Pro, GPT-5, Claude Opus 4.1, Qwen 3 text
- **data :** see details
- **evaluation :** see results
- **result :** Beats model on most benchmarks except General VQA. Improved text reasoning performance on Qwen3 32B(Text).
- **contribution :** As if improving text performance wasn't great enough.
- **etc. :**

## Details

<img width="854" height="435" alt="Image" src="https://github.com/user-attachments/assets/ccd02929-c497-4c20-8c16-92a8354b4f2f" />

## architecture

<img width="806" height="654" alt="Image" src="https://github.com/user-attachments/assets/2c23610e-0484-43fc-8924-c7ffc916a5a3" />

- ViT: SigLIP-2 continual training with dynamic resolution (2D RoPE)
  - -SO400M default / -Large as 2B, 4B model
- MLP Mergedr -- two layer, compress 2x2 feature -- DeepStack
- Interleaved MRoPE -- see (https://github.com/long8v/PTIR/issues/241 , https://arxiv.org/abs/2502.05173)
- DeepStack 
  - https://arxiv.org/abs/2406.04334
- Putting intermediate features from ViT into LLM. Not in every layer, but three times. Architectural changes that were immediately abandoned in 3.5
- Video Timestamp
- We applied time sync MRoPE in #239, but creating temporal position ids for absolute time was quite sparse, especially for long videos, and 2) it was difficult to train on different FSPs when we tried to train this way.
- So the proposed approach is that each video temporal patch is prefixed with a timestamp expressed as a formatted text string-e.g., <3.0 seconds>. -- putting a natural language time stamp between the vision embedding.
- While learning, I also included the hh:mm:ss format.

### Pretraining 
<img width="814" height="187" alt="Image" src="https://github.com/user-attachments/assets/a7261942-ef52-464c-ad69-513b103a5a24" />

- SigLIP2 further learning is omitted
- Stage 0
- high quality caption, visual knowledge collection(? what?), OCR data
- Stage 1 (8K)
   - VL + text-only 
   - a small amount of video data for temporal understanding
- Maybe the seq len is small and that's why you didn't put video?
- Stage 2 (32K)
  -  adjust data mixture to support long-context tasks
- The text-only percentage has increased, while VL data has increased with video and agent-oriented instruction following data.
- Cited this stage as important for learning the ability to reason about long videos
- Stage 3 (262K)
   - text + long-video + long-document

### Pretraining Data
- Image Caption and Interleaved Text-Image Data
- Create a professional captioning model with Image Caption Model 2.5-32B
  - object attributes, spatial layouts, and contextual semantics  
  - Deduplication is performed exclusively on the recaptioned text using semantic similarity metrics, ensuring removal of redundant samples without sacrificing visual diversity.
  - we apply clustering over visual embeddings to identify sparse regions in the data distribution and perform targeted augmentation  
- Interleaved data
- scraping multimodal docs on the web
- Classify domains with a Qwen-based scorer
- Pertaining to pointless articles like ads
- Multimodal parsing for book-scale interleaved data and merging consecutive pages to create 256K tokens
- Remove pure-text or low-alignment segments (maybe CLIP score?)
- Set minimum page count / minimum image-to-text ratio to handle ultra-long sequences
- Knowledge
  - large-scale pretraining dataset centered on well-defined entities spanning more than a dozen semantic categories—including animals, plants, landmarks, food, and everyday objects such as vehicles, electronics, and clothing
- More famous entities were said to be tuned to be sampled more frequently
- I think it was an effort to better understand the entity, but I don't know what it did.
- OCR / Grounding and Counting / Spatial Understanding and 3D Recognition / Code Omissions
- Video
  -  <img width="828" height="459" alt="Image" src="https://github.com/user-attachments/assets/06bf39ca-4a50-4500-bbad-edab5d6f48ae" />
  - Dense Caption Synthesis: 
- How did we create the `short-to-long` caption? Was it a timestamped interleaved short caption or another model?
- You said you were trying to create a consistent story-level description anyway.
    - For long video sequences, we employ a short-to-long caption synthesis strategy to generate holistic, timestamp-interleaved, and temporally coherent story-level descriptions. Leveraging in-house captioning models, we further produce fine-grained annotations that jointly capture event-level temporal summaries and segment-specific visual details
  - Spatio-Temporal Video Grounding
    -  We curate and synthesize large-scale video data annotated at the levels of objects, actions, and persons to strengthen the model’s spatio-temporal grounding capabilities, thereby improving its capacity for fine-grained video understanding.
- STEM data
- The basic policy is to get good at fine-grained visual perception first, and then independently develop linguistic reasoning capabilities.
  - visual perception data
- Create a geometric diagram with programmatic rendering
- I've been working hard on ensembling a capturing model and verifier.
  - multi-model reasoning data
- 12M multimodal reasoning to create long CoT problem solving problem data (with what?)
- Retained the original rollout of the strong reasoning model to preserve continuity and the richness of the reasoning process.
- rule-basd / model-based to filter out ambiguous answers or code-switching (you mean switching between languages?)
- rejection sampling, leaving only challenging problems.
- linguistic reasoning data
- We also use the same data we used in Qwen3
- Agent

## Post Training
SFT (including CoT data) -> Stong-to-weak Distilation -> RL

### SFT data
- To learn a 256K context length, it is said to have been trained with 32K by 1 width first, increased to 256K, and then trained with long context input + 32K token input interleaving.
- SFT
- query filtering / rule and model based answer filtering was said to be done
- Long CoT cold start data
  - Difficulty curation
- Told that only samples with a low pass rate or longer response were kept
- Filtered out problems that can be solved without vision (Qwen3-30B-nothink)
- It says it filters out incorrect answers and those with 1) too much repetition 2) language mixing 3) clear shots.

#### Strong-to-Weak Distilation
- off-policy
- In the first step, ask the teacher model to pull a response and then distil it
- on-policy
- In the second step, have the student similarly follow the logit drawn by the teacher with kl divergence

#### RL
- Data
  - We curate training data from both open-source and proprietary sources and apply rigorous preprocessing and **manual annotation** to ensure high-quality RL queries
- I can't believe you did a manual annotation.
- Take the best performing ones currently out there, take 16 samples, and discard all of them that are wrong or over 90% correct.
- Then, after running RL on a per-task basis, it clears data sources with limited performance improvement.
  - We shuffle and combine task-specific datasets to construct mixed-task batches, ensuring a consistent, predefined ratio of samples per task. The ratio is determined through extensive preliminary experiments.
- Reward system
- Prompt well to get the format right, and give a code switching penalty to prevent reasoning in a different language than the prompt.
- algorithm
- We use an algorithm called SAPO

####  General RL
Centered on two axes
- Instruction following
- Preference Alignment

And after doing SFT, we use it to Fi things like not being able to count numbers or understanding clocks that are weirdly learned.
We also intentionally created and improved data that targets bad behaviors like language mixing, excessive repetition, and formatting issues.

In this case, reward is
- Rule-based
- Heavily heuristic to give high precision feedback without ambiguity
-  Model-based 
  - Qwen2.5-VL-72B-Instruct
- Gives a GT reference and lets you score the quality on multiple axes. Gives good coloring to avoid false negatives.

#### Thinking with image
- Aiming to do multi-turn tool-integrated RL
- Receive three reward signals
  - answer accuracy
  - multi-turn reasoning reward
  - tool-calling reward

## Result
- VLM Bench
<img width="588" height="908" alt="Image" src="https://github.com/user-attachments/assets/bcf8188b-300a-42fe-9fbe-3ad79805f44f" />

- text Bench
<img width="609" height="866" alt="Image" src="https://github.com/user-attachments/assets/6e479144-7388-41c1-9f3e-59440fd0aee7" />

## Ablation
- Additional CLIP learning ablation
It's not that different. But how do you learn Qwen3 without RoPE?
<img width="692" height="149" alt="Image" src="https://github.com/user-attachments/assets/c2a356da-8dff-4002-a1e0-95f87e9074a5" />

- DeepStack
<img width="709" height="141" alt="Image" src="https://github.com/user-attachments/assets/1a7ae52e-3d7f-46a2-b664-96088f344e74" />

Overall, it looks good and I'm seeing a lot of performance improvements in Docs.

- NiaH
<img width="703" height="334" alt="Image" src="https://github.com/user-attachments/assets/7c116028-aa6a-49ce-8cbd-528fcd856c52" />
 
