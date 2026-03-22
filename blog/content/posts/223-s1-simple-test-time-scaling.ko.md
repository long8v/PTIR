---
title: "[202] s1: Simple test-time scaling"
date: 2025-02-10
tags: ['25min', 'test-time-scaling', 'reasoning', '2025Q1']
paper: "https://arxiv.org/pdf/2501.19393"
issue: 223
issueUrl: "https://github.com/long8v/PTIR/issues/223"
---
<img width="689" alt="Image" src="https://github.com/user-attachments/assets/5751e883-620f-47fd-ac8c-4f4c2a223ef8" />

[paper](https://arxiv.org/pdf/2501.19393), [code](https://github.com/simplescaling/s1)

## TL;DR
- **I read this because.. :** 언급되어
- **task :** reasoning in LLM
- **problem :** 어떻게 하면 간단하게 test time scaling을 할 수 있을까?
- **idea :** 데이터 필터링 잘 하자. inference할 때 원하는 길이까지 안나오면 `wait`을 넣어주고, 너무 길면 강제로 eot를 넣어주자(Budget Forcing)
- **architecture :** Qwen2.5-32B-Instruct
- **objective :** ce loss (SFT only)
- **baseline :** OpenAI o1 series, DeepSeek r1 series, QwQ-32B-preview, Sky-T1-32B-Preview, Bespoke-32B, Google Gemini 2.0 Flash Thinking Experimental // 
- **data :** s1K(proposed) -- NuminaMATH, AIME, OlympicArena, OmniMath, AGIEval + 추가로 [스탠포트 통계학과 박사  자격 시험](https://statistics.stanford.edu/)과 [PuzzledQuant](https://www.puzzledquant.com/)란 홈페이지에서 크롤링
- **evaluation :** AIME24, MATH500, GPQA diamond 
- **result :** 학습 샘플 개수 대비 좋은 성능. quality, difficulty, diverse 기준 모두 사용해야 성능이 좋음. 제안한 
- **contribution :** 1) SFT만으로도 test-time-scaling이 되는것을 확인 2) 필터링 관련 ablation
- **etc. :**

## Details
- thumbnail
<img width="684" alt="Image" src="https://github.com/user-attachments/assets/942cb71f-972c-47ef-97b8-023ac07ce0da" />

<img width="1317" alt="Image" src="https://github.com/user-attachments/assets/8921eac0-0f21-438d-b552-26f54ad26fb5" />

### reasoning data curation to create s1k
  - inital collection of 59K
    - NuminaMATH, AIME, OlympicArena, OmniMath, AGIEval + 추가로 [스탠포트 통계학과 박사  자격 시험](https://statistics.stanford.edu/)과 [PuzzledQuant](https://www.puzzledquant.com/)란 홈페이지에서 크롤링
    - 8-gram으로 deduplicate
  - final selection of 1K sample
    - quality: api error, formatting issue(e.g. scii art diagrm, non-existent image reference, incosistent question numbering) --> 51K 남음
    - difficulty: Qwen2.5-7B/32B-Instruct를 사용해서 풀게하고 Claude 3.5 sonnet으로 평가. Qwen 2.5 tokenizer 기준으로 긴 것을 어렵다고 가정하고 필터링. --> 25K 남음
    - diversity : Claude 3.5 Sonnet으로 수학 및 과학(biology, physics, economics) 분류를 나눔(geometry, dynamic system, ... ) --> 24K 남음
      - 추가로 difficulty의 철학에 따라 longerreasoning trace인 걸로 domain 별로 하나의 문제를 뽑음 
    - 결론적으로 50개 도메인이 남음
      - <img width="1209" alt="Image" src="https://github.com/user-attachments/assets/ec3fe146-2fe7-409d-9861-158b73fbab00" />


###  proposed budget forcing

<img width="654" alt="Image" src="https://github.com/user-attachments/assets/1e7cb8d0-db67-4bf3-835f-af6a2cf00aa1" />

### Result
- overall

<img width="600" alt="Image" src="https://github.com/user-attachments/assets/fe0b4253-b2d2-4214-8586-ab4afd55dc64" />

w/o BF에 비해서 성능이 오르며 QwQ-32B란 전체적으로 성능이 비슷한듯.
AIME은 상대적으로 성능이 약하고 MATH500은 성능이 거의 o1 급. GPQA diamnond랑 AIME은 성능이 애매한 것 같은데 sky-t1보다는 좋고 bespoke보다는 MATH는 약하다. 전반적으로 sample efficient하다가 contribution.

- budget forcing
<img width="597" alt="Image" src="https://github.com/user-attachments/assets/4ee742db-29fb-4132-b9fa-96649b58b80e" />

- filtering ablation 
<img width="577" alt="Image" src="https://github.com/user-attachments/assets/c42fb0e0-fd01-40ea-85e2-b9f3ce5a34f4" /> 

- w/ parallel scaling
<img width="1342" alt="Image" src="https://github.com/user-attachments/assets/0dadc20d-0902-40f3-92f2-7187804274f8" />

<img width="598" alt="Image" src="https://github.com/user-attachments/assets/08807b43-b02d-4b9f-afa3-4ad9bee1d6b8" />