---
title: "[218] Qwen2.5-VL Technical Report"
date: 2025-11-10
tags: ['alibaba', 'MLLM', '2025Q2', 'qwen']
paper: "https://arxiv.org/abs/2502.13923"
issue: 239
issueUrl: "https://github.com/long8v/PTIR/issues/239"
summary: "It's been a while since I read it, but just re-reading the video part - efficient ViT variant with many domain abilities"
---
<img width="878" height="286" alt="Image" src="https://github.com/user-attachments/assets/8fa1ddb0-0f0f-4c9b-8da8-0fcd323ab585" />

[paper](https://arxiv.org/abs/2502.13923)

## TL;DR
- **I read this because.. :** It's been a while since I read it, but I just re-read the video part.
- **task :** MLLM --> GUI agent, grounding, video understanding 
- **problem :** better open source model!
- **idea :** more various data, efficient ViT, MRoPE
- **input/output :** {image, video, question} -> answer
- **architecture :** custom ViT (window attention, native resolution(2D-RoPE)) + Qwen2.5 LLM
- **objective :** SFT -> DPO
- **baseline :** priority models (Claude3.5, GPT4o), InternVL, Qwen2-VL
- **data :** interleaved, image-, video QAs, long context videos, ...
- **evaluation :** {text, image, video} bench, GUI, grounding, OCR bench
- **result :** almost all bench SOTA
- **contribution :** efficient ViT variant with many domain abilities
- **etc. :**

## Details
### architecture

<img width="713" height="633" alt="Image" src="https://github.com/user-attachments/assets/becbb89c-a39c-4341-a1da-ce2e93109667" />

<img width="855" height="611" alt="Image" src="https://github.com/user-attachments/assets/9b0861b2-3aa6-4345-9f04-b80e5567d5ab" />

- For efficient computation, only 4 layers see full attention and windowed attention is 112 x 112 (8 x 8 patches)
- Start over from CLIP pretraining
- Now that I look at it, all models see the same ViT.
- <img width="648" height="221" alt="Image" src="https://github.com/user-attachments/assets/b0a0b7b2-8036-4383-b9bc-18dcdb6019cc" />
- Keep the MRoPE introduced in Qwen2-VL, but make it dependent on absolute time (how many seconds into the frame) instead of depending on the input frame.

### data 
- pretraining
- Grounding Data with Absolute Position Coordinates
- Document Omni-Parsing Data
- Video Data
- Enable dynamic sampling of FPS when training.
- For videos longer than 30 minutes, use multi-frame caption to generate video captions
- For video grounding data, include both second-based, hour-minute-second-frame format
- Agent data  

### training recipe

<img width="868" height="306" alt="Image" src="https://github.com/user-attachments/assets/84e4573d-c561-4e89-b449-b3812a070765" />

- Given that the vision encoder has relatively fewer parameters and that we introduced window attention to further reduce its computational demands, we focused on balancing the computational load of the LLM across different GPUs.
- Specifically, we dynamically packed data samples based on their corresponding input sequence lengths to the LLM, ensuring consistent computational loads. In the first and second phases, data were uniformly packed to a sequence length of 8,192, while in the third phase, the sequence length was increased to 32,768 to accommodate the model’s enhanced capacity for handling longer sequences

- rejection sampling for enhanced reasoning 

### Post-training 
- SFT / DPO

### Performance 
- video bench
  - <img width="918" height="485" alt="Image" src="https://github.com/user-attachments/assets/a2d65ed4-dca7-4279-935a-b76a733a1e0d" />
  - Video-MME 
     - https://video-mme.github.io/home_page.html
     - multiple video domain
     - 0 seconds ~ 60 minute (min 1017 seconds)
     - perception, recognition, OCR, temporal reasoning
     - 2700 QA Pairs.  
- The videos are sampled at 2 fps, and the upper limit is 480 frames. So it's like this, but if I pull at 2 fps and go over 480, I don't pull after that?
- Probably MCQA
   - Video-MMMU
- https://videommmu.github.io/ a bit more of an education/knowledge domain
     - art, humanities, medicine, business, question, engineering
- Seems like it's mostly educational video. Maybe MCQA
  - MMMU
    - https://arxiv.org/abs/2501.12380
- Similar to MMVU-Video
    - expert-annotated questions spanning 27 subjects across four core disciplines: Science, Healthcare, Humanities & Social Sciences, and Engineering
  - MVBench
    - https://arxiv.org/abs/2311.17005
    - Spatial Understanding, Temporal Understanding
- video source: Perception, CLEVERER, MiT V1, STAR, Charades-STA -- not looking so good
  - MMBench-Video
    - https://mmbench-video.github.io/
    - perception / reasoning 
- video duration: 0min to 6min -- too short to look good
- There are many video categories, such as people, news, science, advertisement, ...
  - LongVideoBench
    - https://longvideobench.github.io/
    - The LongVideoBench highlights **referred reasoning questions**, which are dependent on long frame inputs and cannot be well-addressed by a single frame or a few sparse frames
- Lots of unusual tasks, such as referring to people in specific frames (questions are relatively fine-grained)
- num videos 3763, eval QAs 6678, avg duration 473 s -- looks good with lots of long ones
    - domain: life, movie, knowledge, news
  - LVBench
    - https://lvbench.github.io/
- avg 4101 sec / 1549 QAs
    - multi-domain (including sports domain)
- temporal grounding, entity recognition, key information retrieval, reasoning, .. -- seems relatively practical!
  - EgoSchema
    - https://arxiv.org/pdf/2308.09126
    - egocentric video
  - Perception Test
- https://arxiv.org/pdf/2305.13786 / videos about stuck things / robotic data
  - MLVU
    - https://arxiv.org/pdf/2406.04264
    - multi-domain
- close-ended task: NeedleQA, PlotQA, action order, action count - doesn't seem that practical
- open-ended task: video summarization, sub-scene captioning, anomaly recognition (fighting on CCTV)
  - TempCompass
    - https://arxiv.org/abs/2403.00476
- Doesn't seem practical. action, fine-grained action, attribute change, event order, direction
- Looks more like low-level vision
  - Charades-STA
    - https://huggingface.co/datasets/VLM2Vec/Charades-STA
- As if the task is to find out if the timestamp was mentioned when the caption was present.
- Is there such a thing as a temporal grounding task?
 
- spatial
  - <img width="919" height="523" alt="Image" src="https://github.com/user-attachments/assets/ba304e39-ea76-4965-9790-152eeae5e07e" />
  
- OCR related
  - <img width="938" height="476" alt="Image" src="https://github.com/user-attachments/assets/f223956a-bf36-4d5a-b56f-a9410caef9b5" />
  
- pure image
  - <img width="929" height="465" alt="Image" src="https://github.com/user-attachments/assets/5dc45e7c-ebf4-4f54-9343-21876ff60bdd" />
  
- pure text
  - <img width="828" height="448" alt="Image" src="https://github.com/user-attachments/assets/604b10c1-de1b-4bdd-9247-8a9cc843d486" />

 