---
title: "[222] Qwen3-VL Technical Report"
date: 2026-03-09
tags: ['MLLM', 'qwen', '2025Q4']
paper: ""
issue: 243
issueUrl: "https://github.com/long8v/PTIR/issues/243"
---
<img width="831" height="278" alt="Image" src="https://github.com/user-attachments/assets/e6eb3007-9c0f-4290-be48-0c1b768ac14e" />

[paper]( )

## TL;DR
- **I read this because.. :** 읽은건 오래됐지만 휘발되고 있는 것 같아서 정리함.
- **task :** MLLM 
- **idea :** arch 변화, 모달리티별 balance를 위해 square-root reweighting 
- **input/output :** {text, image, video} -> text
- **architecture :** interleaved-MRoPE, DeepStack, textual timestamp for video temporal grounding / Dense(2B, 4B, 8B, 32B), MoE(30B-A3B, 235B-A22B)
- **objective :** CE loss -> GSPO 
- **baseline :** Gemini 2.5 Pro, GPT-5, Claude Opus 4.1, Qwen 3 text
- **data :** see details
- **evaluation :** see results
- **result :** 벤치마크 상에서 General VQA 빼고는 대부분 model을 이김. Qwen3 32B(Text)의 text reasoning 성능을 개선시킴. 
- **contribution :** 텍스트 성능 개선시킨게 대단한듯.
- **etc. :**

## Details

<img width="854" height="435" alt="Image" src="https://github.com/user-attachments/assets/ccd02929-c497-4c20-8c16-92a8354b4f2f" />

## architecture

<img width="806" height="654" alt="Image" src="https://github.com/user-attachments/assets/2c23610e-0484-43fc-8924-c7ffc916a5a3" />

- ViT: SigLIP-2 continual training with dynamic resolution (2D RoPE)
  - -SO400M default / -Large as 2B, 4B model
- MLP Mergedr -- two layer, compress 2x2 feature -- DeepStack
- Interleaved MRoPE -- (https://github.com/long8v/PTIR/issues/241 , https://arxiv.org/abs/2502.05173)를 보면 됨
- DeepStack 
  - https://arxiv.org/abs/2406.04334
  - ViT의 중간 feature를 LLM에 넣어주는 방식. 모든 레이어에 넣어주는 것은 아니고 세번 정도 넣어줌. 3.5에서 바로 폐기된 아키텍쳐 변화
- Video Timestamp
  - #239 에서 time sync MRoPE를 적용했었는데 absolute time에 대해 temporal position id를 만들어 보니까 특히 긴 비디오에 대해 상당히 sparse했고 2) 이 방식 대로 학습을 하려다 보니 다양한 FSP에서 학습하는게 어려웠음
  - 그래서 제시한 방식은 each video temporal patch is prefixed with a timestamp expressed as a formatted text string—e.g., <3.0 seconds>. -- vision embedding 사이에 자연어 time stamp를 넣는 것임.
  - 학습 중에는 hh:mm:ss format도 같이 넣어서 학습했음.

### Pretraining 
<img width="814" height="187" alt="Image" src="https://github.com/user-attachments/assets/a7261942-ef52-464c-ad69-513b103a5a24" />

- SigLIP2 더 학습한건 생략되어 있음
- Stage 0
  - high quality caption, visual knowledge collection(? 뭘까?), OCR data  
- Stage 1 (8K)
   - VL + text-only 
   - a small amount of video data for temporal understanding
    - 아마 seq len이 작아서 video를 안넣은게 아닐까?
- Stage 2 (32K)
  -  adjust data mixture to support long-context tasks
    - text-only 비율이 늘었다고 하고 VL data는 video와 agent oriented instruction following data가 늘었다고 함. 
    - 이 stage에서 long video에 대해 reason하는 능력을 학습하는데 중요했다고함
- Stage 3 (262K)
   - text + long-video + long-document

### Pretraining Data
- Image Caption and Interleaved Text-Image Data
  - Image Caption Model을 2.5-32B로 전문 캡셔닝 모델을 만듦
  - object attributes, spatial layouts, and contextual semantics  
  - Deduplication is performed exclusively on the recaptioned text using semantic similarity metrics, ensuring removal of redundant samples without sacrificing visual diversity.
  - we apply clustering over visual embeddings to identify sparse regions in the data distribution and perform targeted augmentation  
- Interleaved data
  - web에서 multimodal doc 긁음
  - Qwen based scorer로 도메인 분류
  - 광고 같은 무익한 문서들 피렅링함
  - book-scale의 interleaved data를 위해 멀티모달 parsing을 하고 연속 Page를 합쳐서 256K token을 만듦
  - pure-text or low-alignment segments(아마 CLIP score이지 않을까?)를 지움 
  - ultra-long sequence를 처리하기 위해 minimum page  count / minimum image-to-text ratio를 정함
- Knowledge
  - large-scale pretraining dataset centered on well-defined entities spanning more than a dozen semantic categories—including animals, plants, landmarks, food, and everyday objects such as vehicles, electronics, and clothing
  - 더 유명한 Entity는 더 자주 sampling되도록 조정했다고 함
  - entity를 더 잘 이해하기 위한 노력인 것 같은데 뭘했다는건지 모르겠음.
- OCR / Grounding and Counting / Spatial Understanding and 3D Recognition / Code 생략
- Video
  -  <img width="828" height="459" alt="Image" src="https://github.com/user-attachments/assets/06bf39ca-4a50-4500-bbad-edab5d6f48ae" />
  - Dense Caption Synthesis: 
    - 어덯게 `short-to-long` caption을 만들었을 까? short caption 을 이어붙여서 timestamped interleaved로 만든걸까 아님 또 모델을 쓴걸까
    - 여튼 일관성 있는 story-level desrcirption을 만드려고 했다고 함
    - For long video sequences, we employ a short-to-long caption synthesis strategy to generate holistic, timestamp-interleaved, and temporally coherent story-level descriptions. Leveraging in-house captioning models, we further produce fine-grained annotations that jointly capture event-level temporal summaries and segment-specific visual details
  - Spatio-Temporal Video Grounding
    -  We curate and synthesize large-scale video data annotated at the levels of objects, actions, and persons to strengthen the model’s spatio-temporal grounding capabilities, thereby improving its capacity for fine-grained video understanding.
- STEM data
  - 기본적인 정책은 fine-grained visual perception을 먼저 잘하고 그다음에 linguistic reasoning capability를 독립적으로 하는 것. 
  - visual perception data
    - geometric diagram을 programmatic rendering으로 만듦
    - 캡셔닝 모델과 verifier를 엄청 ensemble해서 열심히 만듦
  - multi-model reasoning data
    - long CoT problem solving problem 데이터를 만들기 위해 12M multimodal reasoning데이터를 만듦 (뭘로?)
    - 연속성과 reasoning process의 풍부함을 살리기 위해 strong reasoning model의 Original rollout을 그대로 사용함.
    - rule-basd / model-based로 ambigious answer나 code-switching(? 언어 중간에 바뀌는거 말하는건가) 필터링 함
    - rejection sampling으로 challenging problems만 남김.
- linguistic reasoning data
  - Qwen3에서 사용한 데이터도 그대로 사용함
- Agent

## Post Training
SFT (including CoT data) -> Stong-to-weak Distilation -> RL

### SFT data
- 256K context length를 학습하기 위해 32K로 1에폭 먼저 학습하고, 256K 로 늘린 뒤에 long context input + 32K token input interleaving 해서 학습했다고 함.
- SFT
  -  query filtering / rule and model based answer filtering 했다고함
- Long CoT cold start data
  - Difficulty curation
    - low pass rate or longer response를 가진 샘플만 남겼다고함
    - vision 없이도 풀수 있는 문제를 필터했다고 함 (Qwen3-30B-nothink) 
    - 정답이 틀린 것과 1) 과한 반복 2) language mixing 3) clear하게 찍은 것들을 필터링 했다고 함.

#### Strong-to-Weak Distilation
- off-policy
  - 첫 단계에서 teacher model한테 response 뽑으라 한 뒤 distil 함
- on-policy
  -  두번째 단계에서 teacher가 뽑은 Logit을 student가 kl divergence로 비슷하게 따라가게 함 

#### RL
- Data
  - We curate training data from both open-source and proprietary sources and apply rigorous preprocessing and **manual annotation** to ensure high-quality RL queries
    - ㄷㄷ manual annotation을 했다니
  - 현재 나와있는 것들 중 가장 성능이 높은 걸 가져와서 16 sample 씩 뽑은 뒤 모두가 틀리거나 90% 이상 맞춘 것은 지워버림.
  - 그리고 태스크별로 RL을 돌린 뒤에 성능 개선이 한정적인 데이터 소스는 지워버림.
  - We shuffle and combine task-specific datasets to construct mixed-task batches, ensuring a consistent, predefined ratio of samples per task. The ratio is determined through extensive preliminary experiments.
- Reward system
  - format을 잘맞추게 하기위해 프롬프트를 잘 주고, prompt랑 다른 언어로 reasoning하는 걸 막기 위해 code switching penalty도 줌
- algorithm
  - SAPO 라는 알고리즘을 씀

####  General RL
두 축을 중심으로 함 
- Instruction following
- Preference Alignment

그리고 SFT를 하고 나서 이상하게 학습된 숫자를 못센다던가 시계를 이해를 못한다던가 하는 것들을 Fi하는데 사용함
또한 language mixing, 과한 반복, 포매팅 이슈 같은 안좋은 행동을 막기위해 일부러 그것을 타겟한 데이터를 만들어서 개선함.

이때 reward는 
- Rule-based
  - 애매모호 하지 않은 high precision feedback을 주기 위해 열심히 휴리스틱을 짬 
-  Model-based 
  - Qwen2.5-VL-72B-Instruct
  - GT reference를 주고 여러 축으로 qulity를 점수매기도록 함. false negative를 만들지 않는데 좋은 영햐을 줌. 

#### Thinking with image
- multi-turn tool-integrated RL을 하는걸 목표로 함
- 아래 세개의 Reward signal을 받음
  - answer accuracy
  - multi-turn reasoning reward
  - tool-calling reward

## Result
- VLM 벤치
<img width="588" height="908" alt="Image" src="https://github.com/user-attachments/assets/bcf8188b-300a-42fe-9fbe-3ad79805f44f" />

 - text 벤치
<img width="609" height="866" alt="Image" src="https://github.com/user-attachments/assets/6e479144-7388-41c1-9f3e-59440fd0aee7" />

## Ablation
- 추가 CLIP 학습 ablation
뭐 그렇게 차이 안나네. 근데 RoPE 안쓰고 Qwen3 어케 학습함?
<img width="692" height="149" alt="Image" src="https://github.com/user-attachments/assets/c2a356da-8dff-4002-a1e0-95f87e9074a5" />

- DeepStack
<img width="709" height="141" alt="Image" src="https://github.com/user-attachments/assets/1a7ae52e-3d7f-46a2-b664-96088f344e74" />

전반적으로 괜찮아지고 Doc류에서 성능 개선이 많이 일어나 보인다. 

- NiaH
<img width="703" height="334" alt="Image" src="https://github.com/user-attachments/assets/7c116028-aa6a-49ce-8cbd-528fcd856c52" />
 
