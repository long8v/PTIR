---
title: "[184] Improve Vision Language Model Chain-of-thought Reasoning"
date: 2024-10-29
tags: ['CMU', 'MLLM', '2024Q3']
paper: "https://arxiv.org/abs/2410.16198"
issue: 203
issueUrl: "https://github.com/long8v/PTIR/issues/203"
---
<img width="990" alt="image" src="https://github.com/user-attachments/assets/7f580442-a1e9-46de-b6b9-b1f639569585">

[paper](https://arxiv.org/abs/2410.16198)

## TL;DR
- **I read this because.. :** reasoning ability in VLM
- **task :** VLM
- **problem :** VLM instruction data 대부분이 단문이다
- **idea :** GPT4-o를 가지고 CoT 데이터를 만들자
- **architecture :** LLaVA-NeXT
- **objective :** CE loss -> DPO loss
- **baseline :** LLaVA-NeXT, GPT4o, Cambrian, (data) RLAIF
- **data :** ShareGPT4-o Reasoning(아직 공개 안함)
- **evaluation :** A-OKVQA, DocVQA, ChartQA, AI2D, ScienceQA, ... 
- **result :** 모든 벤치에서 골고루 높은 성능. 
- **contribution :** 적은 데이터셋으로 벤치마크 개선. reasoning 관련 분석 많이 함

## Details
- motivation
<img width="1228" alt="image" src="https://github.com/user-attachments/assets/4fd38f06-0281-4925-827a-04d08f4527f1">

### Data
- reasoning data distilation 
<img width="396" alt="image" src="https://github.com/user-attachments/assets/5143e33b-5c41-45a3-8a98-3dfa538e47a7">

<img width="511" alt="image" src="https://github.com/user-attachments/assets/6f93ef00-095a-4d4d-bf4f-843ca2dcb4a5">

<img width="1227" alt="image" src="https://github.com/user-attachments/assets/b917283e-f042-4d05-ad19-d4a7ea01b02b">

<img width="1302" alt="image" src="https://github.com/user-attachments/assets/9d903ebe-0b9b-4670-b563-803f62e315be">


### Result
<img width="575" alt="image" src="https://github.com/user-attachments/assets/e0658b2a-d569-4621-a17b-df66c25ad7b1">

위와 같은 데이터 구성
- (1) format: 답변 포맷만 맞출 수 있는 수준으로 구성한 것. 9개의 데이터셋 별로 50개의 sampling을 함. CoT / direct 둘다 + LLaVA-pretrain에서 2K
- (2) direct data: (1) + 답변이 바로 나오는 193K를 Full로 넣은 것
- (3) CoT data : (1) + CoT 193K를 넣은 것 + 추가로 GLLaVA-align / QA
- (4) CoT SFT : (1) + direct + CoT 둘다 넣은 것 + 추가로  GLLaVA-align / QA


<img width="1107" alt="image" src="https://github.com/user-attachments/assets/f2d3ec4a-27cb-4d15-8bb4-72db547b94fc">

**CAN REASONING BE IMPLICITLY LEARNT FROM DIRECT PREDICTION?** -- (1)과 (2) 비교
-> direct answer만 넣고 학습한 경우 CoT infererence를 할 경우에 개선이 미미하거나 오히려 떨어지는 경우도 있었음(mathvista -1.7)

**HOW EFFECTIVE IS COT REASONING DATA?**
-- (3) chartQA나 Mathvista같이 계산이 많이 들어가는 벤치마크에서 성능이 올랐고, 의외로 TextVQA, DocVQA, InfoVQA 같은 Text-heavy한 벤치마크에서도 성능이 오르는걸 볼 수 있음.
-- (4) CoT와 Direct 모두 학습을 했을 때 가장 평균 성능이 좋았다. 다만 TextVQA, DocVQA, AI2D는 direct 성능이 더 좋았다. fact extraction 위주로 뽑는 벤치마크여서 그런 것 같다고 추정.


**ABLATION TESTS ON DATA COMPOSITION**
<img width="459" alt="image" src="https://github.com/user-attachments/assets/c5f25ed4-64ec-4aa9-8eba-9a9f6ff7e4f0">

수학 쪽 data ablation. text only sft는 별로 효과가 없어서 제거했다고 함

<img width="462" alt="image" src="https://github.com/user-attachments/assets/f2610c8b-8a7a-4195-af54-63a89fd8fc35">

science 쪽 ablation. 둘다 같이 쓰면 서로 좋았다.

**Comparsion of GPT4o / Cambrian**
<img width="614" alt="image" src="https://github.com/user-attachments/assets/6c883fce-405a-44a9-a4a4-1317f88fa687">

ScienceQA는 closed set 이 성능이 좋네. train data 문제일수도..

### DPO Result
<img width="1107" alt="image" src="https://github.com/user-attachments/assets/97050261-dad2-4965-b1fb-20661b847416">

<img width="743" alt="image" src="https://github.com/user-attachments/assets/36cb7c26-8f44-4840-b84b-31e97666d928">

<img width="1121" alt="image" src="https://github.com/user-attachments/assets/74198e0e-ed30-447c-a469-18d55fc25f55">

외에 BoN등 내용이 더 많은데 나중에 정리 ㅜㅜ 