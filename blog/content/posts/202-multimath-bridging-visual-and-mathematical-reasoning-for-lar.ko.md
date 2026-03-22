---
title: "[183] MultiMath: Bridging Visual and Mathematical Reasoning for Large Language Models"
date: 2024-10-24
tags: ['MLLM', '2024Q3', 'STEM']
paper: "https://arxiv.org/abs/2409.00147"
issue: 202
issueUrl: "https://github.com/long8v/PTIR/issues/202"
---
![image](https://github.com/user-attachments/assets/0412b82b-7d5e-47c8-b208-f1bde13e7723)

[paper](https://arxiv.org/abs/2409.00147), [code](https://github.com/pengshuai-rin/multimath)

## TL;DR
- **I read this because.. :** mathvista 개선을 위해
- **task :** LVLM
- **problem :** 기존의 math 관련 LVLM work인 G-LLaVA, Math-LLaVA는 각각 geometric reasoning 능력에 제한, CoT 능력에 제한이라는 단점이 있다
- **idea :** 다양한 수학 분야 + CoT를 추가한 데이터셋을 만들자 
- **architecture :** llava (clip-vit-large, DeepSeekMath-RL)
- **objective :** ce loss + ppo loss
- **baseline :** closed LLMs, LLMs, Math LLMs, Open-Source MLLMs(G-LLaVA-7B, Math-LLaVA-13B, LLaVa-1.5-7B, LLaVA-NeXT-34B)
- **data :** (align) LLaVA-Pretrain + geo170k-align (instruct) LLaVA-instruct (math instruct) MultiMath300k-instuction, Geo170k-qa, MathV360k (PPO) MultiMath300K-val, GSM8K-train, Math-train, CMATH-train
- **evaluation :** Mathvista, Mathverse, GSM8K, MATH, CMATH, GaoKao
- **result :** open source model 중 가장 높은 mathvista, mathverse 성능, text math 벤치에서도 다른 MLLM과 비교해봤을 때 sota. 
- **contribution :** 데이터셋 제안 및 text/vision 둘다 높은 성능 
- **etc. :** 내용은 뻔할 수 있지만 분석이 많아서 재밌었다

## Details
### Thumbnail
![image](https://github.com/user-attachments/assets/14e08137-1f35-4a2b-973e-c9d31b28b780)

### proposed MultiMath-300K
![image](https://github.com/user-attachments/assets/bdf2e2f0-db83-40b1-9b9a-13e7326487b7)
![image](https://github.com/user-attachments/assets/5eae65d1-4c08-43c6-b9d9-fef549bb5889)

- 직접 이미지 license 사서 제작(http://test.xuekubao.com/)
- QA 뿐 아니라 captioning 되어 있는 것도 있음 
- geomertry problem solving, automatic theorem proving, mathematical word problems 모두 커버
- 영어/중국어라고 하는데 거의 중국어 인듯..?
- CoT 커버

![image](https://github.com/user-attachments/assets/80782c56-7923-4c09-a9f0-e52c68121bc5)

### 수집 방법
![image](https://github.com/user-attachments/assets/ae4f9bb1-58d1-4f0a-8e34-67881afe2fad)

- round 1: GPT-4o를 사용하여 step-by-step reasoning chains를 생성. 원본 데이터를 힌트로 사용
- round 2: GPT4-o를 사용하여 생성된 reasoning chain이 standard answer와 비교했을 때 잘 생성됐는지 평가. inconsistent하다면 reasoning step을 수정
- round 3: GPT-4o 답변과 standard answer를 사용한 뒤 맞는 정답만 사용.

### training 
- (align) LLaVA-Pretrain + geo170k-align : 1 epoch 
- (instruct) LLaVA-instruct : ViT도 full tuning 
- (math instruct) MultiMath300k-instuction, Geo170k-qa, MathV360k 
- (PPO) MultiMath300K-val, GSM8K-train, Math-train, CMATH-train를 소스로 만듦

Process-supervised RL 
![image](https://github.com/user-attachments/assets/def88bae-771f-4846-aa8a-2125690e11dc)

- CoT reasoning 시켜서 multiple reasoning step을 생성하게 함
- GPT-4o한테 correctness를 평가하게 하고 에러가 발생한 step을 찾아서 맞는 solution을 생성하게 함
- 이걸로 prefer / disprefer set이 나옴 -> RM 학습
PPO 
- 각 actor모델이 생성한 reasoning step에 대한 reward score를 가지고 PPO 학습 

## Result 
![image](https://github.com/user-attachments/assets/c2077f7b-ae56-420e-a44f-2779a0db0e03)

closed model 보단 아니지만 open source model 중 가장 높은 성능

### text 성능
![image](https://github.com/user-attachments/assets/6ebbdf3c-b32b-40f1-a4cc-4a9ad8b7313c)

다른 math 오픈소스 특화 모델들이 LLaVA-NeXT보다 안좋음. 

### contribution of RL

![image](https://github.com/user-attachments/assets/658bfb52-5f77-4fe7-b85a-87eb6e465030)

PPO 단계에서 쓰였던 도메인인 cmath, gsm8k, math 개선, 쓰이지 않은건 개선 안됨. mathvista의 경우 0.8 올랐고 (align, sft는 각각 1.3, 1.6 올림)mathverse의 경우 0.2 떨어짐

### LLM backbone
![image](https://github.com/user-attachments/assets/5cac664d-734a-4ad8-b632-7aaaa78e4924)

vicuna 대비 성능차이가 많이 남. MathVista 42.9 vs 50.0 ㄷㄷ
MultiMath가 중국어가 대부분인 탓도 조금 있을 듯. 그래도 table 3보면 학습이 안된건 아님. 

