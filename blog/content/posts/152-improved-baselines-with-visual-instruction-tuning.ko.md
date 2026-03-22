---
title: "[140] Improved Baselines with Visual Instruction Tuning"
date: 2023-12-12
tags: ['multimodal', 'LLM', '2023Q3', 'MLLM']
paper: "https://arxiv.org/pdf/2310.03744.pdf"
issue: 152
issueUrl: "https://github.com/long8v/PTIR/issues/152"
---
<img width="674" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/460f065f-7d42-49d7-ac8f-160f21f350a8">

[paper](https://arxiv.org/pdf/2310.03744.pdf)

see llava https://github.com/long8v/PTIR/issues/128#issue-1749571159 here

## TL;DR
- **I read this because.. :** aka LLaVA1.5 / ShareGPT4V에서 LLaVA1.5 레시피를 따랐다고 해서 오게 됨 
- **task :** LVLM
- **problem :** LLaVA는 reasoning도 뛰어나고 real-world instruction following도 잘하지만 benchmark에 대해서는 성능이 떨어지는데 이를 개선해보자 
- **idea :** 여러 가지 scale up / VQA 같은 단답에 대해서는 prompt를 좀 더 잘 주도록 하자! 
- **input/output :** image + question -> answer 
- **architecture :** ViT-L/14(336 resolution) + LLaMA 13B
- **objective :** ce loss 
- **baseline :** llava, Qwen-VL, Shikra, BLIP-2, IDEFICS, instructBLIP
- **data :** (alignment) LCS-558K(LAION-CC-SBU with BLIP caption) / (end-to-end finetuning) LLaVA instruction data + VQA(OKVQA, A-OKVQA), OCR(OCRVQA, TextCaps), region-level VQA(Visual Genome, RefCOCO) 
- **evaluation :** GQA, MME, MM-Vet, VQA, GQA, VisWiz, SQA, VQA, POPE, ... 
- **result :** VQA류를 finetuning할 때 넣으니 개선, format prompt를 하니 개선, linear대신 2-layer mlp를 넣으니 개선, resolution을 높이니 개선, ShareGPT 등 다양한 데이터 넣으니 개선(ShareGPT를 넣어서 multilingual 능력도 생김)
- **contribution :** 적은 리소스, open data만으로 괄목할만한 성능을 낸 것.  
- **etc. :**

## Details
### contribution
<img width="410" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b3bf4b04-e997-476d-9c0f-cc15ffc10f07">

최소한의 tuning(1.2M scale의 public data로 8 A100 days로 끝나는)으로 좋은 성능

### Dataset 
- alignment learning
LCS-558K(LAION-CC-SBU with BLIP caption)
중간에 llava-lightning이란게 있었고 수렴을 좀 더 빨리 하기 위한 variant인 듯하다.
https://github.com/haotian-liu/LLaVA/issues/86#issuecomment-1533346022 를 보면 CC랑 대략적으로 수량을 맞췄고 much larger concept converage 해서 수렴을 더 빨리 한다고 한다.
CC랑 blip caption은 text 형태가 많이 다를 것 같긴 한데.. ㅋㅋ 약간 벤치마크를 찍기 위한 잘 보이지 않는 trick이 아닌지? llava 1.5가 conservation에 대한 성능을 안 잰게 아쉽다 아마 훨씬 낮게 나오지 않았을까? 

- end-to-end finetuning
LLaVA instruction data + VQA(OKVQA, A-OKVQA), OCR(OCRVQA, TextCaps), region-level VQA(Visual Genome, RefCOCO) 
몰랐는데 Visual Genome이 VQA가 있었구낭..
https://paperswithcode.com/dataset/visual-genome 
<img width="700" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/9b9b8922-9e78-4dad-8537-74b22373d253">


### Improved baseline of LLaVA
- LLaVA가 벤치마크에서 성능이 안좋았던 이유
VQA는 단답으로 한 두 단어로 끝내야 하는데 LLaVA는 그런 식으로 학습되지 않음 / 데이터를 조금 봄 
-> "response formatting format" 
VQAv2 같은 걸 넣을 때 `Q: {Question} A: {Answer}` 대신 `Answer the question using a single word or phrase`라고 prompt를 줌. 이렇게 해서 단순히 VQAv2를 training data에 넣으니까 특히 MME라는 벤치마크에서 성능이 2배가 됨 502 -> 1197 

<img width="406" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/46dd82ce-094b-430b-a774-87d631c73266">

### Result / Ability 
<img width="815" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/7335f01f-f4f9-4706-a73d-dece262215ea">
LLaVA는 이상하게 대답 

- 관련 없는 이미지에 대해서도 잘 대답 
<img width="394" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a0939a79-84bc-41ee-87ce-6f971d85d717">

- json 뽑기 가능! (ocr 능력)
<img width="401" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5adca21d-40b9-4fc6-a70d-93c74722ded8">
 
- zs multi-lingual 
ShareGPT(https://sharegpt.com/)라는 데이터를 사용해서인지 multilingual instruction을 따르더라 
사용자가 자기가 사용한 chatGPT 질답을 올릴 수 있는 플랫폼 아마 language only 인듯하다.
특히 MMBench-CN에서 실제로 chinese instruction data를 활용한 Qwen-VL-Chat을 이겼다 (신기하네)

- computational cost
6 hours for pretraining / 20 hours for visual instruction tuning using 8A100s 
<img width="400" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/68150561-4413-4fc8-a6be-10229787ec55">


- limitation
1) resolution에 따라 image seq len이 늘어난다는 점. q-former가 그런걸 대체하는데 이건 수렴이 느린 것 같더라. 효율적으로 q-former를 학습할 수 있는 연구가 진행되어야
2) multi image 처리 불가. 데이터가 없다.
3) 여전히 타겟 도메인에 한정되어 있다
4) hallucination이 있다


- d--etails

<img width="395" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b1276863-f34d-44c3-9295-3998b9c5c201">

