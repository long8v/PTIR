---
title: "[174] Evaluations for Object Hallucinations "
date: 2024-09-02
tags: ['survey', 'evaluation', 'MLLM']
paper: ""
issue: 193
issueUrl: "https://github.com/long8v/PTIR/issues/193"
---
<img width="961" alt="image" src="https://github.com/user-attachments/assets/dab5544c-498b-4ef5-a9a3-e79a1c82ff7c">


## CHAIR (== Object HalBench)
[18'EMNLP] Object Hallucination in Image Captioning https://arxiv.org/abs/1809.02156
- COCO caption & semantic segmentation label -- 동의어를 사용해서 captioning model의 hallucination 측정 
- CHAIR_i의 분모는 언급된 모든 object 개수 // CHAIR_s는 문장 개수 
- COCO karpathy / robust test set  
<img width="316" alt="image" src="https://github.com/user-attachments/assets/62d6208b-1b0e-4649-81c4-f99022a1c190">

- 이 논문에서 말하고자 했던건 CIDEr 등 captioning 성능은 높더라도 실제로 hallucination 성능은 이와 비례하지 않는다는 점
- LVLM에서는 RLHF-V가 만든 descriptive 설명을 하라는 8개 프롬프트를 주고 gt segment와 CHAIR를 구하고 이가 Object Halbench로 레포트됨

## POPE
[24'EMNLP] Evaluating Object Hallucination in Large Vision-Language Models https://arxiv.org/pdf/2305.10355
- 위의 CHAIR 같은 object hallucination을 LVLM으로 가져와 측정한 논문 
<img width="367" alt="image" src="https://github.com/user-attachments/assets/f7aa2e0f-f8a0-4e4c-bcc8-ba43666207cb">

- 그런데 이때 prompt를 어떻게 할지에 따라 성능이 들쭉날쭉하다. 그리고 object를 뽑고 GT object랑 매칭하는데 복잡한 Human parsing rule이 필요하다 
- 그래서 제안한 것이 POPE 
<img width="783" alt="image" src="https://github.com/user-attachments/assets/c6cd2e06-ca5c-46e5-8b28-ff6fdd526c4a">

- 캡션을 생성하고 hallucinated object를 찾는게 아니라 yes, no 로 대답할 수 있는 question을 만들어서 측정
- gt label은 semantic label SEEM 같은 것으로 뽑아서 object pool 보강
- 여기에 3가지 negative set을 만듦
  - random : random object class  
  - popular : 학습 데이터에서 많이 나타난 object class
  - adversarial : 현재 등장한 object와 같이 많이 등장한 object class  
- 사용한 set은 COCO에서 object 가 3 개 이상 나오는 subset 500개를 만들었다고
- 이 논문에서 발견한 것은 1) COCO에서 많이 등장한 2) COCO에서 많이 자주 등장한 object hallucination이 심했다고

<img width="646" alt="image" src="https://github.com/user-attachments/assets/807aa545-5c16-4f9e-b46c-98efef24f9bb">

## HallusionBench
[CVPR'24] HallusionBench: An Advanced Diagnostic Suite for Entangled Language Hallucination and Visual Illusion in Large Vision-Language Models https://arxiv.org/abs/2310.14566

## AMBER
[arxiv'24] AMBER: An LLM-free Multi-dimensional Benchmark for MLLMs Hallucination Evaluation
https://arxiv.org/abs/2311.07397

<img width="738" alt="image" src="https://github.com/user-attachments/assets/f072b352-e7e2-43b5-8564-04be806f6d9f">

![image](https://github.com/user-attachments/assets/56e7a701-6f17-42d3-8f82-663acaadd7bd)

![image](https://github.com/user-attachments/assets/837d6646-8446-4682-a718-ea83e8f7b0d4)


두가지가 있음 1) generative 2) discriminative
generative는 Object existence를 위해 고안되었고 discriminative 는 object, relation, attribute 모두 구할 수 있음
미리 이미지와 이에 등장한 object, attribute, relation Label을 다 annotate한 뒤에 discriminative는 yes, no로 그냥 맞춤
generative는 생성된 캡션에 대해 noun parse하고 그 다음에 그냥 CHAIR 인듯.. 흠냐