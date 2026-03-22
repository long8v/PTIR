---
title: "Panoptic Scene Graph Generation"
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

- **task :** Propose a segmentation-based SGG task, panoptic scene graph generation
- **problem :** Many datasets have been proposed for SGG, but bbox-based SGG is problematic because it has a lot of redundant information (e.g. hair) and leaves out background.
- **idea:** propose dataset / propose two-stage, one-stage baseline
- **architecture :** (one-stage baseline) 1) PGSTR: Put a triplet query in DETR and pull it out directly 2) PGSFormer: Create a relation query and an object query, then select the most related objects to the relation by cosine similarity, and use them as the subject, and add two layers of FFNs to the object to form the triplet.
- **objective :** SGG triplet loss. but you gave me something else instead of bbox loss, right?
- **baseline :** two-stage models(IMP, MOTIFS, VCTree, GPSNet)
- **data :** Visual Genome & COCO, and then select the overlapping one, and then create a new annotation -> "PSG dataset"
- **result :** I took the existing two-stage models and applied them to PSG, and the proposed two-stage baseline performs better.
- **contribution :** Building datasets & providing baselines.

## Details
### SGG datasets
![image](https://user-images.githubusercontent.com/46675408/182051990-f7c4c92e-e283-4f28-9620-1eda869e2c22.png)

### PGSTR
![image](https://user-images.githubusercontent.com/46675408/182052158-f1009241-5cf9-47b5-ba8f-5b4e5ed59f37.png)

### PGSFormer
![image](https://user-images.githubusercontent.com/46675408/182052191-c11f20f4-959b-4233-9fb2-cdf4939ad7c2.png)
