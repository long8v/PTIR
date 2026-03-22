---
title: "[120] Large-scale Bilingual Language-Image Contrastive Learning"
date: 2023-06-19
tags: ['2022Q1', 'CLIP', 'multilingual']
paper: "https://arxiv.org/pdf/2203.14463.pdf"
issue: 129
issueUrl: "https://github.com/long8v/PTIR/issues/129"
summary: "multilingual clip - Korean CLIP. learning related some Finding. result part has diffusion also and .. authors are two but multiple analysis bb"
---

<img width="632" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/36493fd1-a8d7-4820-93c9-590f2f9005dc">

[paper](https://arxiv.org/pdf/2203.14463.pdf)

## TL;DR
- **I read this because.. :** multilingual clip
- **task :** multimodal alignment
- **problem :** I want to learn multilingual clips, but the ones made in translation don't capture the characteristics of the country's culture/vocabulary
- Idea:** Collect data to learn
- **input/output :** image + text / similiarity score(for clip)
- **architecture :** image encoder(ViT-B/32) and text encoder(transformer) 
- **objective :** MSE(for MAE) and infoNCE(for CLIP)
- **baseline :** CLIP, UNITER, Visual N-Gram, ImageBERT
- **data :** collect korean {image-text} pair from web + collect available english {image-text pair}
- **evaluation :** image classification / retrieval
- **result :** higher performance in English than clip
- **contribution :** Korean CLIP. learning related some Finding. result part has diffusion as well .. two authors but multiple analysis bb
- **etc. :**

## Details

## motivation

- I want to create a multi-lingual CLIP
- The common approach is to just machine translate the text, which doesn't capture the vocabulary or culture of the country.
- learn english-korean bilingual
- Dataset suggestions
- Suggest a training scheme
- Learn with MAE in 1 step
- Using the multi crop technique
- Some findings
- Even without direct bilingual supervision, the embedding space was still adjusted through the image.
- I found the strong augmentation used in SimCLR to be intrusive.

## training scheme

- CLIP and the other two
- Learn the vision encoder first with MAE instead of directly with contrastive
    
<img width="615" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/09a39f2d-931a-4870-80f4-fe05f7483cc8">

    
- Using multi-crop augmentation
    - standard resolution 224 x 224  / low resolution 96 x 96
- ablation for the above two
    
<img width="584" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/957f0820-bca1-41c9-91c6-c803812e9f34">


## dataset

- english {image-text} pair
    - CUB200
- 37.4M WITs (108 languages)
- YFCC15M (clip filtered at 100M)
    - CC3M
    - CC12M
    - LAION400M
- Create another 70M from the cc web dump, following the way LAION created it
- korea {image - text} pair : 708M scale
- It just says crawled.
- Includes 50M celebrity faces and names
- korea wikipedia inclusion
- Much larger than LAION400M or CLIP's WIT 400M
- as if the dataset would be ≥ 1B in total.

## training detail

- implementation : just pytorch without using anything else
- text encoder
    - GPT-2 style transformer(?) / 63M / 12 layesr / hid dim 512 / 8 heads
        - gpt-2 style transformer
            
            Layer normalization (Ba et al., 2016) was moved to the input of each sub-block, similar to a pre-activation residual network (He et al., 2016) and an additional layer normalization was added after the final self-attention block. A modified initialization which accounts for the accumulation on the residual path with model depth
            is used. We scale the weights of residual layers at initialization by a factor of 1/
            √N where N is the number of residual layers. 
            
- tokenizer : BPE 98K vocab size trained with 2M english/1.5M korean
- (↔ CLIP is 49K)
        
- visual encoder
    - ViT-B/32
    - 256 x 256 ?

- Other hparams

<img width="714" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/0946ae42-6466-4952-a172-303f9d472f64">


- training
    - half precision
- 16 hours to learn 80 A100 → MAE / 362 hours for multimodal training (15 days?)

## Benchmark Dataset

- zs-classification
- Used the benchmark's english label translated to Korean
    - ImageNet / Cifar10 / Cifar100 / CLEVER Counts / Describable Textures Dataset / EuroSAT / FER2013 / Food101 / GTSRB / MNIST / RESIC45 / StanfordCars
    - (in-house data) WebKorean
        - 36,826 images ↔ 428 Korean labels
- zs-retrieval
    - Flickr30k / MSCOCO(english) / MSCOCO(korean)

## result

<img width="716" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/24b7517a-e1c9-470d-8983-b32186ceae07">


- zero-shot classification
- 3.3% higher performance than CLIP on average
- Korean is CLIP performance chaos
- clip is the closest thing to a photo of { }, so we'll categorize it as a photo of { }, and then use
- It's not that I didn't have any Korean data, but it was too small, so I used the
- zero-shot retrieval
- English Korean Both Performance GoodGood

<img width="659" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/715ac104-3a06-4c59-9f6f-c795118960df">


## findings

- Strong augmentations, such as color distortion, perform better for classification, but not for retrieval, which is a higher-level problem.

<img width="540" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/083f86d7-cceb-47f0-9668-2304ee94ca7e">

- Even though I didn't add contrastive loss directly between the two languages, the images were spatially aligned because they were viewed together.
    
<img width="653" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/fcbf102e-7122-4d57-8c06-1d007ce72ccc">

    
- I tried it with diffusion, but it's definitely different for Korean?
- This is a little different from the above result, isn't it?

<img width="687" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/48f5f095-ee88-4221-a476-d2c03544645d">

