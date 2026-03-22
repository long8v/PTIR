---
title: "[212] MiMo-VL Technical Report"
date: 2025-07-02
tags: ['MLLM', 'reasoning', '2025Q2']
paper: "https://arxiv.org/abs/2506.03569"
issue: 233
issueUrl: "https://github.com/long8v/PTIR/issues/233"
---
<img width="665" alt="Image" src="https://github.com/user-attachments/assets/1a8adacd-f766-4054-aeae-ef996201fc43" />

[paper](https://arxiv.org/abs/2506.03569), [code](https://github.com/XiaomiMiMo/MiMo-VL)

## TL;DR

* **I read this because.. :** AIME을 report한 LVLM2
* **task :** 멀티모달 이해, 추론, GUI grounding
* **problem :** reasoning과 understanding 모두 잘하는 모델 
* **idea :** 대규모 pretrain + rl
* **input/output :** {(image, video), prompt}→ answer or action
* **architecture :** Qwen2.5-ViT + MLP projector + MiMo-7B
* **objective :** CE loss(pretrain, SFT), on-policy GRPO(RL)
* **baseline :** Qwen2.5-VL, InternVL3, GPT-4o, UI-TARS 등
* **data :** 2.4T token for pretraining(caption, interleaved, ocr, grounding, gui, synthetic reasoning) 
* **evaluation :** 50+ 벤치마크 (MMMU, OlympiadBench, GUI 등)
* **result :** 대부분 벤치마크에서 타 모델 압도, 오픈소스 중 최고 Elo
* **contribution :** 
* **etc. :** task 간 interference 문제 제기, long-context 대응 가능


## Details
### architecture 

<img width="848" alt="Image" src="https://github.com/user-attachments/assets/b874b1ca-7d69-4ba1-acd7-528a1138ddaf" />

- strong reasoning abilities inherent in MiMo-7B-Base (Xiaomi, 2025), enabling their seamless transfer and adaptation to multimodal contexts. Consequently, this allows our model to exhibit powerful and versatile multimodal reasoning capabilities across a broad array of domains. -> 이미 mimo가 base지만 Reasoning ability가 있다는 것 같음. 

### training

<img width="631" alt="Image" src="https://github.com/user-attachments/assets/ba557164-96b9-4353-9243-387b19930d47" />

stage 4에서 32K까지 올림

#### pre-training
2.4T token 학습 
- implement dedicated data curation pipelines tailored to the characteristics of each data type
- data
  - Image Caption Data : dedup (image perceptual hashing), text filtering, re-caption(w/ linguistic consistency, repititon filtering, imbalance filtering (w/ MetaCLIP)
  - interleaved data: webpages, books, academic papers, pdf parsing, knowledge density and readability filtering, ...
  - ocr : to increase learning difficulty, handwritten, typographically deformed, blury occluded, bounding box annotated
  - grounding data: single / multiple objects
  - video: publicly available, video recaptioning, dense finegrained, event distribution, challenging question about video and synthesize response
  - GUI data : open source & synthetic. grounding, action
  - synthetic reasoning : image, prompt는 오픈소스로 모으고 생성에는 MiMo-7B-base를 사용. answer 의 정답 뿐 아니라 thought의 clarity를 평가하고, redundancy 제거, consistent formatting을 하도록 strict filtering.

#### post-training 
![Image](https://github.com/user-attachments/assets/29c59096-912d-4b30-b5fe-4ce697532a8f)
 
- RLVR
  - data
    - visual reasoning: open source & k-12 collection
      - LLM is prompted to filter proof-based problems and rewrite multiple-choice questions with numerical or symbolic answers into free-answer formats, alleviating potential reward hacking
    - text reasoning : include more challenging queries requiring college or competition-level intelligence (than visual reasoning, K12)
    - Image Grounding: GIoU or point가 box안에 들어오는지
    - Temporal Video Grounding : video moment retrieval [mm:ss,mm:ss] -- IoU
- RLHF
- mixed on-policy RL
  - RLVR + RLHF 둘이 합쳐서 GRPO로 학습 
  - GRPO와 다른 점은 완벽히 on-policy (vllm을 매번 새로 띄움)을 사용해서 clipping이나 importance sampling 부분이 없음
    -  <img width="449" alt="Image" src="https://github.com/user-attachments/assets/1004a22b-54b7-4600-bd0d-f6a0319b5c0a" />
    - <img width="308" alt="Image" src="https://github.com/user-attachments/assets/6751ba2f-d54a-4313-a095-643814ff7fb4" />
    - c.f. GRPO
     -  <img width="1271" alt="Image" src="https://github.com/user-attachments/assets/0a1ae91c-fc5d-47b1-ba4d-ed7f6c3f717c" />


### performance

<img width="623" alt="Image" src="https://github.com/user-attachments/assets/19b8677b-0ad2-4c6e-9572-97a8ef3e3d3c" />

RL 단계에서 크게 재미는 못봄 

<img width="643" alt="Image" src="https://github.com/user-attachments/assets/7a131113-5afc-42d2-bc78-687942b93a89" />



### ablation

<img width="670" alt="Image" src="https://github.com/user-attachments/assets/eda60ef1-0c93-4d1f-839a-20212eac7d7b" />

KL term이 없어서 그런건지? 

<img width="627" alt="Image" src="https://github.com/user-attachments/assets/ae025ed5-2c48-41fd-9ea9-3af828bb6d5c" />

### challenges 
- Interference Between RL Tasks: grounding task 같은건 grounding 궤적이 길지 않고 reasoning 은 길어서 서로 반대 방향으로 움직여서 각각을 하는 RL 만큼의 성능을 확보하기가 어려웠다고 함

<img width="793" alt="Image" src="https://github.com/user-attachments/assets/8ca058fd-3936-41e8-984c-46cdb41a2a97" />

mimo 7B-rl의 aime24 68.0 ~ 80.1 (max len 48K) https://huggingface.co/XiaomiMiMo/MiMo-7B-RL

(이 논문에서는 67점) 