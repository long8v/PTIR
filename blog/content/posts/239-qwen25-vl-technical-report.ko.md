---
title: "[218] Qwen2.5-VL Technical Report"
date: 2025-11-10
tags: ['alibaba', 'MLLM', '2025Q2', 'qwen']
paper: "https://arxiv.org/abs/2502.13923"
issue: 239
issueUrl: "https://github.com/long8v/PTIR/issues/239"
---
<img width="878" height="286" alt="Image" src="https://github.com/user-attachments/assets/8fa1ddb0-0f0f-4c9b-8da8-0fcd323ab585" />

[paper](https://arxiv.org/abs/2502.13923)

## TL;DR
- **I read this because.. :** 읽은지는 좀 됐지만 video 쪽만 다시 읽음
- **task :** MLLM --> GUI agent, grounding, video understanding 
- **problem :** 더 나은 open source model!
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

- 효율적인 연산을 위해 4 layer만 full attention을 보고 windowed attention은 112 x 112(8 x 8 patches)  
  - CLIP pretraining 부터 다시 함 
- 지금 보니까 모든 모델이 같은 ViT를 보는군
- <img width="648" height="221" alt="Image" src="https://github.com/user-attachments/assets/b0a0b7b2-8036-4383-b9bc-18dcdb6019cc" />
- Qwen2-VL에서 도입된 MRoPE를 그대로 쓰되 input frame에 dependant한게 아니라 absolute time에 dependant(실제 몇초 째의 Frame인지)를 넣도록 함 

### data 
- pretraining
- Grounding Data with Absolute Position Coordinates
- Document Omni-Parsing Data
- Video Data
  - 학습 시 FPS를 dynamic하게 sampling하도록 함.
  - 30분을 넘어가는 비디오의 경우 multi-frame caption을 통해 비디오 캡션을 생성함
  - video grounding data의 경우 second-based, hour-minute-second-frame format 둘다 넣게 함 
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
     - The videos are sampled at 2 fps, and the upper limit is 480 frames. 이렇게 되어있는데 그럼 2 FPS로 뽑고 480 넘어가면 그 뒤는 안뽑는건가?
     - 아마 MCQA
   - Video-MMMU
     - https://videommmu.github.io/ 조금 더 교육/지식 도메인에 가까움
     - art, humanities, medicine, business, question, engineering
     - 거의다 educational video 쪽인듯. 아마 MCQA
  - MMMU
    - https://arxiv.org/abs/2501.12380
    - MMVU-Video와 비슷한듯
    - expert-annotated questions spanning 27 subjects across four core disciplines: Science, Healthcare, Humanities & Social Sciences, and Engineering
  - MVBench
    - https://arxiv.org/abs/2311.17005
    - Spatial Understanding, Temporal Understanding
    - video source: Perception, CLEVERER, MiT V1, STAR, Charades-STA -- 별로 좋아보이진 않음
  - MMBench-Video
    - https://mmbench-video.github.io/
    - perception / reasoning 
    - video duration: 0min~6min -- 너무 짧아서 별로 좋아보이지 않음
    - video category는 여러가지 있는듯, people, news, science, advertisement, …
  - LongVideoBench
    - https://longvideobench.github.io/
    - The LongVideoBench highlights **referred reasoning questions**, which are dependent on long frame inputs and cannot be well-addressed by a single frame or a few sparse frames
      - 특정 프레임에 있는 인물을 refer하는 등 조금 특이한 task가 많음 (질문이 비교적 finegrained함)
    - num videos 3763, eval QAs 6678, avg duration 473 s -- 긴 것들이 많아서 좋아보임
    - domain: life, movie, knowledge, news
  - LVBench
    - https://lvbench.github.io/
    - avg 4101초 / 1549 QAs
    - multi-domain (including sports domain)
    - temporal grounding, entity recognition, key information retrieval, reasoning, .. -- 비교적 실용적이여 보임! 
  - EgoSchema
    - https://arxiv.org/pdf/2308.09126
    - egocentric video
  - Perception Test
    - https://arxiv.org/pdf/2305.13786 / 멈춰진 사물에 대한 비디오 / robotic data
  - MLVU
    - https://arxiv.org/pdf/2406.04264
    - multi-domain
    - close-ended task : NeedleQA, PlotQA, action order, action count — 그렇게 까지 실용적이어 보이진 않음
    - open-ended task: video summarization, sub-scene captioning, anomaly recognition (CCTV에서 싸우고 있음)
  - TempCompass
    - https://arxiv.org/abs/2403.00476
    - 실용적이지 않아보임. action, fine-grained action, attribute change, event order, direction
    - low-level vision에 가까워보임
  - Charades-STA
    - https://huggingface.co/datasets/VLM2Vec/Charades-STA
    - 캡션이 있을 때 timestamp에 대해 나왔는지 찾는 task인듯
    - temporal grounding task가 이렇게 없나?
 
- spatial
  - <img width="919" height="523" alt="Image" src="https://github.com/user-attachments/assets/ba304e39-ea76-4965-9790-152eeae5e07e" />
  
- OCR related
  - <img width="938" height="476" alt="Image" src="https://github.com/user-attachments/assets/f223956a-bf36-4d5a-b56f-a9410caef9b5" />
  
- pure image
  - <img width="929" height="465" alt="Image" src="https://github.com/user-attachments/assets/5dc45e7c-ebf4-4f54-9343-21876ff60bdd" />
  
- pure text
  - <img width="828" height="448" alt="Image" src="https://github.com/user-attachments/assets/604b10c1-de1b-4bdd-9247-8a9cc843d486" />

 