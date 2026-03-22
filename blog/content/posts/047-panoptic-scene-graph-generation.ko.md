---
title: "[41] Panoptic Scene Graph Generation"
date: 2022-08-01
tags: ['dataset', 'SGG', '2022Q3', '25min']
paper: "https://arxiv.org/pdf/2207.11247.pdf"
issue: 47
issueUrl: "https://github.com/long8v/PTIR/issues/47"
---
![image](https://user-images.githubusercontent.com/46675408/182051767-7cc81412-dd89-4d10-a242-757d391ab52d.png)

[paper](https://arxiv.org/pdf/2207.11247.pdf), [dataset](https://psgdataset.org/), [code]( https://github.com/Jingkang50/OpenPSG)

## TL;DR
![image](https://user-images.githubusercontent.com/46675408/182051976-74a38015-648b-4f58-822c-603194822b9d.png)

- **task :** segmentation 기반 SGG 태스크인 panoptic scene graph generation 제안
- **problem :** SGG를 위한 데이터셋들이 많이 제안되었지만 bbox 기반의 SGG는 의미없이 중복되는 정보(e.g. hair)가 많고, background는 빼고 있어서 문제가 있다. 
- **idea :** 데이터셋 제안 / two-stage, one-stage baseline 제안
- **architecture :** (one-stage baseline) 1) PGSTR: DETR에 triplet query 넣고 바로 뽑기 2) PGSFormer: relation query와 object 쿼리를 만든 뒤, cosine 유사도로 relation과 가장 관련 높은 object들을 뽑은 뒤에 이를 subject로 두고 object는 두 층의 FFN추가해서 triplet을 구성. 
- **objective :** SGG triplet loss. 근데 bbox loss 대신에 다른거 줬겠지?
- **baseline :** two-stage models(IMP, MOTIFS, VCTree, GPSNet)
- **data :** Visual Genome & COCO 중 겹치는거 뽑은 다음에 어노테이션 새로 함 -> "PSG dataset"으로 명명
- **result :** 기존 two-stage 모델들 가져다가 PSG에도 적용해봤는데 제안한 two-stage baseline이 성능이 더 좋음
- **contribution :** 데이터 셋 구축 & 베이스라인 제공.

## Details
### SGG datasets
![image](https://user-images.githubusercontent.com/46675408/182051990-f7c4c92e-e283-4f28-9620-1eda869e2c22.png)

### PGSTR
![image](https://user-images.githubusercontent.com/46675408/182052158-f1009241-5cf9-47b5-ba8f-5b4e5ed59f37.png)

### PGSFormer
![image](https://user-images.githubusercontent.com/46675408/182052191-c11f20f4-959b-4233-9fb2-cdf4939ad7c2.png)
