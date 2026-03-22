---
title: "[143] Honeybee: Locality-enhanced Projector for Multimodal LLM"
date: 2023-12-22
tags: ['kakao', '2023Q4', 'MLLM']
paper: "https://arxiv.org/pdf/2312.06742.pdf"
issue: 155
issueUrl: "https://github.com/long8v/PTIR/issues/155"
---
<img width="788" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5174178f-8ae5-47f4-9d3c-5ea8ffec9fa7">

[paper](https://arxiv.org/pdf/2312.06742.pdf)

## TL;DR
- **I read this because.. :** data recipe에 대해서 ablation을 잘했다고 해서 읽음 
- **task :** MLLM 
- **problem :** projector는 seq len이 길어지는 효과가 있고 resampler 구조는 local-aware한 능력이 없어서 점수가 떨어지는 것 같다
- **idea :** linear projection 대신 conv나 deformable attention을 사용하자 
- **input/output :** image, text(query) -> text(answer)
- **architecture :** CLIP ViT-L/14 + ResNet or DDETR(약간의 변경) + LLM(Vicuna-7B / 13B)
- **objective :** LM loss
- **baseline :** LLaVA, MiniGPT-4, LLaMA-Adatper2, mPLUG-owl, InstructBLIP, IDEFICS, Shikra, Qwen-VL, LLaVA-1.5
- **data :** (pretraining) COYO100M, BLIP-CapFilt (instruction) captioning(BlipCapFilt, COYO100M), VQA-open(VQAv2, GQA, OCRVQA, VSR), VQA-mc(SicenceQA, A-OKVQA), REC(RefCOCO, RefCOCO+, RefCOCOg, VG), Instruction(LLaVA150K, ShareGPT)
- **evaluation :** SEED(사지선다), MME, MMB(binary), LLAVAW
- **result :** sota
- **contribution :** resampler의 약점을 파악하고 개선. 다양한 레시피 관련 팁 공유(혜자 논문..)
- **etc. :** 준범님 참여한 논문 다 좋은듯..

## Details
- motivation 
<img width="547" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/c6452755-e41c-4b97-982a-2204d1c5a266">

벤치마크들 중 spatial 관련 애들 linear projection vs resampler 대한 분석
resampler 애들이 spatial을 못한다는 분석. finer detail들이 sampler 과정에서 사라진다.
반면에 linear 스타일은 local 정보까지 잘 전달하는 경향이 있다

### Honey-bee
<img width="1015" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/88d988cc-17ea-4ac0-a3e6-a5cfcc67dc8f">

 - MLLM objective

 <img width="477" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a8d542ba-b34f-41da-9a58-f741d58827a2">

- architecture

1) vision encoder 2) projector 3) large language model

- efficieny of mllm
대부분의 병목(메모리 소비, throughput)이 LLM에서 걸림. 즉 LLM에 건내주는 visual token 수가 efficiency를 결정함. 

<img width="496" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/45911fd4-5250-409f-a94a-06481c31c3f3">

<img width="510" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/0ab1f1c0-5177-4617-ba98-e7583871ee09">

예를 들어 linear projection은 파라미터가 거의 없지만, 같은 # tokens resampler랑 시간이 비슷함. 즉 학습 시간은 # tokens랑 비례함
resampler의 # visual token이 늘어남에 따라 한 step 학습하는데 시간이 오래걸리는 모습 
(llava에서 주장하는 파라미터가 적어서 금방 수렴한다랑 약간 다른 포인트의 논지. 거긴 파라미터가 적어서 "수렴"을 얘기하고 여긴 그냥 당장 학습 속도를 의미)

- proposed

motivation에서 나온 이야기처럼 resampler 구조가 locality를 반영을 못하는 것 같다. locality를 반영할 visual projector를 추가해주자

- Abstractor 
<img width="460" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/44d70363-a302-4ad2-807e-7715315cae50">

C-abstractor는 ResNet
D-abstractor는 Deformable Attention

결과
<img width="500" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4f87d6d5-eb0e-4f66-ac30-3cd8447049e8">


### Training 
전체적으로 llava-like training strategy
- Pre-training for vision-language alignment.
COYO와 BlipCapFilt를 1:1 (이런 비율은 manual하게 짧게 학습해보고 정했다고 함)
projector만 학습

- visual instruction tuning
projector와 LLM 같이 학습 
데이터는 아래와 같음
<img width="485" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/8fdac703-b5af-46b3-ab80-6db9964a4032">

<img width="427" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/847204f8-a910-4a03-9333-15c4e804076b">


###  Hidden Recipe for Visual Instruction Tuning
<img width="638" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/dc7c4fd2-9186-46eb-ad14-374f632cf464">

- Dataset Combination
  - 다양하는게 쓰는게 좋고
  - 특히 open-ended VQA류를 뺐을 때 벤치마크 성능이 많이 떨어짐
  - multiple-choice VQA류를 빼면 MMB, SEED가 많이 떨어짐 -> aligning response patterns에 중요  
  - captioning data를 빼면 LLAVAW가 많이 떨어짐 -> LLAVAW가 narrative and descriptive responses를 선호함
  - visual or text instruction-following datasets 하면 LLaVAW(GPT로 평가시키는거)가 떨어짐.

<img width="369" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/48cc0512-9977-442f-bd30-d9fd651b6417">

- Dataset Balancing
  - pretraing 할 때는 1:1 
  - instruction에서는 manually tune 할 수 밖에 없다 ㅜㅜ  
<img width="450" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/2fb50411-fec2-4a80-a4f8-0916094180a4">

VSR, ShareGPT, ScienceQA, OCRVQA는 절대적이 양이 적어서 비율을 줄임
OCRVQA, VG는 실험적으로 줄임 
Captioning에 BlipCapFilt을 뺀건 cost 때문이었지만 ablation 해봤을 때 성능이 떨어지진 않았음 (!! alt-text를 취하고 caption을 버렸군)
 
- Instruction vs Multi-task
<img width="416" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/3218e109-ff32-4e86-993f-3bb27d105989">

instruction을 주는 식으로 하냐 vs 데이터셋이나 태스크 이름으로 주는 식으로 하냐에서 instruction이 더 좋았다

- template

<img width="415" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/db38de3b-e178-43e4-8986-2c8319fc7a64">

granularity는 "task"별로 template을 다르게 쓰는 것이 좋았다 (!!)
template을 여러개 쓰는 것보다 하나만 쓰는게 좋았다 (!!) 
flip은 QA 순서를 바꾸는 식인데 별로 도움이 안됐다

- multi-turn
<img width="414" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/246eca15-8ff9-4060-bbf4-343217bc596e">

VQA류 같은건 multi-turn으로 만드는게 좋았다. 특히 비슷한 질문들 dedup까지 하니까 아주 좋았다
<img width="860" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5f9b242d-b04d-43e0-b8af-c2b8d911be4f">


- Evaluation
<img width="382" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/39349ad4-8ace-4789-8c6c-4f64b9356027">


### D-etails
- examples of benchmarks
<img width="466" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/fb5f984d-3990-461a-b1fd-7827911e79cc">


SEED가 fine-grained한게 많다고 하네 

- resampler의 architecture 디자인
<img width="336" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/28905c98-33a9-4dbd-bd05-6c0f0faad81b">

- Templates
<img width="686" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/2d137ca3-bd87-481b-a18b-65369045304e">

캡션류는 별도 프롬프트 없이 
VQA, REC task는 fine-grained하게 바꿈
가령 [Visual Semantic Reasoning](https://paperswithcode.com/dataset/vsr)에서 The cat is inside the refrigerator, False를 Is the cat inside the refrigerator?를 No 형식으로 바꿈
그리고 이미 instruction용으로 나온건 template없이 그대로 사용  
