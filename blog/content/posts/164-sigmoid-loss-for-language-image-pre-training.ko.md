---
title: "[152] Sigmoid Loss for Language Image Pre-Training"
date: 2024-03-12
tags: ['25min', 'CLIP', '2023Q1']
paper: "https://arxiv.org/ftp/arxiv/papers/2303/2303.15343.pdf"
issue: 164
issueUrl: "https://github.com/long8v/PTIR/issues/164"
---
<img width="981" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/f0ae6e83-f4b8-4d63-a167-5bd050db47b4">

[paper](https://arxiv.org/ftp/arxiv/papers/2303/2303.15343.pdf), [code](https://github.com/google-research/big_vision)

## TL;DR
- **I read this because.. :** CLIPScore 관련해서 SigLIP의 score는 softmax로 학습된 것과 많이 다르려나? loss 부분과 효과가 궁금해서 읽음
- **task :** CLIP
- **problem :** InfoNCE 함수 내에 들어가는 softmax가 학습적으로 불안정하며, 분모의 negative pair를 합하는 과정에 all-gather가 들어가는데 그게 학습 비효율을 야기시킴. 
- **idea :** sigmoid loss 제안. 아래 좀 더 상술 
- **input/output :** {image, text} -> score
- **architecture :** ViT-B/16, (LiT 셋팅) ViT-B/8, ViT-g/14 
- **objective :** Sigmoid Loss
- **baseline :** CLIP, OpenCLIP, EVA-CLIP, CLIPA-v2
- **data :** WebLI dataset using only English image and text pairs
- **evaluation :** ImageNet-1k / COCO R@1 
- **result :** 비교군보다 좋은 성능.  데이터가 다르긴 함. ㅋㅋ 자세히 못봤지만 step수는 맞췄겠징..
- **contribution :** sigmoid loss 제안. 다양한 ablation 실험. 
- **etc. :**

## Details
### Sigmoid Loss
기존 InfoNCE
<img width="448" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a2026a48-3f24-4084-a323-07edbdf331b1">

여기서 image -> text / text -> image를 위해 summation이 각각의 axis로 두 번 이루어진다는 점.

<img width="350" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/87b87103-71d4-455c-b301-1df8b13ce7f3">

제안한 sigmoid loss. 여기서 $z_{ij}$는 positivie일 때 1 negative일때 -1인 label.
negative가 너무 많기 때문에 imbalance를 해결하기 위해 $t'$, $b$를 두었고 이는 log10과 -10으로 초기화 함. 

언뜻 보면 negative 다 계산해야되기 때문에 softmax 연산이랑 차이가 있나 싶다만
<img width="979" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4b694b37-bd4f-4d5e-9d92-8eebf3cf1337">

이런 식으로 chunking을 하면 softmax의 경우 분모분을 계산하기 위해 feature를 all_gather하는 게 필요함. 그런데 sigmoid loss의 경우 negative pair가 loss에는 들어가지만 positive pair에 대해 negative pair가 필요한건 아니기 때문에 그냥 chunking해서 forward 하면 되어서 더 효율적임.

<img width="700" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/e6cc8dab-249c-491b-a773-83db69d49931">

LiT 셋팅에서 softmax보다 낫고, 그냥 CLIP 셋팅에서도 적당히 작은 bs에 대해서 softmax보다 나음.

### Performance

<img width="350" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/3f7c1945-d072-433c-92db-f447e5ea4b84">

<img width="695" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/11554026-aa35-4d68-920b-f08e292a2994">


### Ablations
<img width="692" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/8bd9aa8d-a39b-4ad3-a957-8ea82452e14e">

perturbation에 더 강하다고 함 

<img width="694" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/9d6ecb2b-1967-498c-ac1c-bfab9be51e1e">

- hard : 어려운 sample들을 masking하는 전략
- Hard, matched pairs : masking하면 실제로 학습 시 보게 된 pair 수가 적게 되므로 sample 수를 맞춘 내용 

hard negative로 하면 유독 더 좋은 벤치마크가 있으려나 궁금함 
