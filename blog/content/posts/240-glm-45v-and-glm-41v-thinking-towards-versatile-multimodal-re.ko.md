---
title: "[219] GLM-4.5V and GLM-4.1V-Thinking: Towards Versatile Multimodal Reasoning with Scalable Reinforcement Learning"
date: 2025-11-12
tags: ['RL', 'MLLM', '2025Q3']
paper: "https://arxiv.org/abs/2507.01006"
issue: 240
issueUrl: "https://github.com/long8v/PTIR/issues/240"
---
<img width="606" height="234" alt="Image" src="https://github.com/user-attachments/assets/0bb4672e-05c1-4cec-a0c8-f92f4eb065be" />

[paper](https://arxiv.org/abs/2507.01006), [code](https://github.com/zai-org/GLM-V)

## TL;DR
- **I read this because.. :** 비교적(?) 최신 MLLM 모델이자 RL을 열심히 깎은 모델. 지인이 써봤더니 좋다고 해서 읽어봄.
- **task :** MLLM with thinking 
- **problem :** good MLLM model
- **idea :** multi-modal pretraining -> cold start SFT -> RL (RLVR + RLHF). 데이터를 열심히 모으자
- **input/output :** {image, video, question} -> answering 
- **architecture :** VE (AIMv2-Huge), LLM (GLM-4-9B-0414, GLM-4.5-Air)
- **objective :** CE loss -> GRPO loss 
- **baseline :** Qwen2.5-VL, Kimi-VL, InternVL3, GPT-4o, Gemini... 
- **data :** pretraining data 50M -> SFT (??) -> RL (??)
- **evaluation :** (image) general VQA, STEM, OCR-chart, long-doc, grounding, GUI agent, coding(Design2Code, Flame-React-Eval), (video) VideoMME, MMVU, LVBench, MotionBench 
- **result :** 동급 모델 중엔 SOTA
- **contribution :** 특히 RL단계에서 여러 시행착오나 lesson learned를 잘 정리했다. kimi 처럼 rl을 좋아하는듯. 또 VLM에서 생기는 문제들에 대해서도 잘 정리해줘서 고마움.. 근데 왜 RL은 training step이 없지.
- **etc. :**

## Details
### architecture

<img width="616" height="448" alt="Image" src="https://github.com/user-attachments/assets/2221d865-e5ee-41e2-b308-f6c21fe603ee" />

- VE (AIMv2-Huge), GLM-4-9B-0414, GLM-4.5-Air
- 3D conv (w, h, temporal) — if image is duplicated (stride 2여서 single image는 그냥 두개 복사해서 temporal 축에 넣은듯 )
- 2D-RoPE in ViT + original absolute PE (bicubic interpolation)
- LLM에선 RoPE를 3D-RoPE 로 바꿔서 spatial understanding을 하게 함 (w, h, n번째 토큰?)

### pretraining stage
- data (최종적으로 50M) 
image caption, interleaved, OCR data, Grounding data, Video data, instruction tuning data. 
  - Video data
    - corpus from academic, web, proprietary sources
    - standard caption은 hallucination이나 omission이 많으므로 finegrained human annotation으로 complex action이나 in-scene text를 annotate하도록 파이프라인을 개발함 (caption이 아니라 다른 annotation을 맡겼다는 것 같음?) 
    - 더 깊은 visual 이해를 이해 camera motion 이나 shot composition 과 같은 cinematic elements를 human-in-the-loop workflow로 annotate함. 
    - 비디오 길이는 따로 없는듯 
- training
  - multimodal pre-training (seq len 8192) — 120K step -> long-context continual pre-training (seq len 32K) — global step 10K 1.5 bs

### SFT stage
- high-quality CoT reasoning examples 
  - almost chinese and english
  - filter with pretrained model (too easy or excessively hard)
  - data filtering도 빡세게 하고 iterative data enhancement도 함 (RL하고 그 모델로 다시 cold-start data만들고..)
- training 
  - full param tuning
  - seq len 32K 
  - global bs 32
  - also includes high-quality text-only long-form SFT data. 
  - GLM-4.5V는 think / no-think할 수 있는 모델이어서 /nothink를 user prompt로 넣으면 thinking content가 empty가 되도록 학습하게 함.

### RL stage
- reward
  - RLVR과 RLHF (model-based rewards)를 조합함
  - The extraction of the final answer in RLVR : LLM으로 extraction하는게 think가 길어지면 어려울 수 있어서 <|begin_of_box|>{FINAL_ANSWER}<|end_of_box|>로 파싱했다고 함. \boxed{}도 final answer가 길어짐에 따라 어려웠다고 함 
  - 도메인 별로 열심히 reward 깎음 ..
  - <img width="841" height="321" alt="Image" src="https://github.com/user-attachments/assets/27808b2a-dc17-4ff3-908b-7fe362f0fe5a" />
- algorithm    
  - GRPO
  - no KL(KL이 text-only와 다르게 빠르게 상승하는 경향이 있었으나 kl term을 넣으면 성능이 제한되었다고), no entropy bonus, clip higher, larger BS 
- training recipe 
  - RL with Curriculum Sampling (RLCS), dynamic sampling extension with ratio EMA, no KL and entropy loss
- lesson learned
  - we discover that when training a unified VLM across diverse skills, any weakness in the reward signal for a single capability can derail the entire training (figure 5)
    - 이게 재밌는 부분인데 여러 도메인 합쳐서 학습하다보니 하나라도 reward가 hacking 될 여지가 있거나 하면 모델이 전반적으로 성능이 안좋게 됐다고 함
    - 그렇기 때문에 각각의 도메인에 대해 run을 돌리고 -> Reward 를 잘받나 rollout 확인하고 등등 이런 Iteration을 돌았다고 함 ㅜㅜ 
    - A coarse or incomplete reward design can lead the model to discover shortcuts for boosting its reward rather than truly improving its task performance.
      -  가령 llm-as-a-judge reward(여기서 RLHF)를 쓰는데 "counting task"를 하는 경우 response가 "정답은 1부터 10 사이의 숫자야" 와 같이 rollout하는 경우가 있었다고 함.. ㅎㅎ 
    - <img width="608" height="414" alt="Image" src="https://github.com/user-attachments/assets/ef426232-6e1a-4db5-adf4-46d4b64e0b79" />
  - The peak performance in the RL phase does not perfectly correlate with a cold-start SFT model’s performance.
  - Domain interference in RL is less pronounced than in SFT. 

### result 

<img width="561" height="854" alt="Image" src="https://github.com/user-attachments/assets/66f0d0bc-0ff2-4327-873e-ce2e21bc21a4" />

- evaluation 보면 academic에 가까운 MMVU나 VideoMMMU의 경우 think 를 킬 때 각각 4점, 6점 정도의 상승이 있지만 긴 비디오 task인 LVBench나 MVBench의 경우 direct 평가가 더 성능이 좋고 VideoMME도 성능 개선이 거의 없다 싶음. 이미지 bench 중 STEM 류는 역시 성능이 높으나 general VQA는 그렇게까지 아닌 느낌. 
- 평가를 위해 대부분 vLLM을 썼지만 video inference를 위해 sglang 사용 
- vision token max는 image 6K video는 48K 사용. 
- parsing 등 api가 필요한 경우 모두 GPT4o 사용. 다른 모델들도 똑같이 평가.

<img width="587" height="365" alt="Image" src="https://github.com/user-attachments/assets/64cd4f91-fe92-4656-821b-c186d4e5700f" />

- RL의 효과 cross-domain 성능 개선 — 모든 도메인 다 섞으면 더 좋아짐

<img width="568" height="829" alt="Image" src="https://github.com/user-attachments/assets/e3417af6-0f17-4a82-9266-e90925ce398b" />

- 10B under에선 거의 sota긴 하네 
