---
title: "GIT: A Generative Image-to-text Transformer for Vision and Language"
date: 2022-06-26
tags: ['multimodal', 'microsoft', '2022Q2']
paper: "https://arxiv.org/pdf/2205.14100.pdf"
issue: 36
issueUrl: "https://github.com/long8v/PTIR/issues/36"
---
![image](https://user-images.githubusercontent.com/46675408/175830566-0182206a-d8fa-4fdb-a8c6-02f8499a4f9c.png)
[paper](https://arxiv.org/pdf/2205.14100.pdf)

## TL;DR
- Problem :** Pre-training for MLM, Image-Text Matching, etc. is different from the downstream tasks. For this reason, there are approaches that solve with a unified generative model, usually with a multi-modal encoder and a text decoder.
- Idea :** Train generatively with only one image encoder and text decoder. Let the image classification also result from a generative model rather than a closed vocabulary. In this case, let's learn Swin-like encoders in contrast.
- **result :** SOTA in image/video captioning, question answering.
![image](https://user-images.githubusercontent.com/46675408/175831072-2632c3f4-e75f-48d4-9cdc-ea054f5b9458.png)
- **contribution :** captioning seq2seq simple structure without cross attention, that it is SOTA in QA.

## Details
### Architecture 
![image](https://user-images.githubusercontent.com/46675408/175831699-f1f83fd3-0faf-4177-bff3-3413172303e1.png)
- pre-training
The image encoder is based on a contrastive pre-trained model (Florence), the image is flattened from a 2D feature map and projected to the D dimension through a linear layer and a layernorm layer. The text decoder is just a transformer. The image features are concatenated with the text embedding and fed into the transformer input. The image and text tokens are masked as shown below so that the image tokens attend each other and the text only sees all the image tokens and the preceding text tokens.
![image](https://user-images.githubusercontent.com/46675408/175831875-aedb862e-03ef-4ae5-9888-67948496297a.png)

For each image-text pair, given an image, we proceed by predicting the text token as LM given the image. The loss is the cross-entropy loss.
- finetuning
The same LM task finetune, only the input is slightly different.
- Image captioning is trained exactly the same as pretrain.
- VQA concatenates the question and GT asnwer and puts it in like a special caption, with the loss imposed only on the answer token.
- In the image classification task, instead of having a classifier, we leave the class name as in image captioning and let it learn auto-regressively. This generation-based model is easier when new categories are added or deleted.

### Data
- COCO
- Conceptual Captions(CC3M)
- SBU
- Visual Genome(VG)
- ALT200M

### Related works
- The difference with CoCa is that they both do a contrastive, generation task, but CoCa combines losses, whereas this model does it sequentially.
- Flamingo and GIT both have one image encoder and one text decoder, but the difference is that Flamingo concatenates the representation of the simple image encoder and the representation of the text decoder into the decoder, rather than adding cross-attention in a separate decoder. Also, Flamingo freezes the pretrained weight of the image/text and only finetunes cross-attention, whereas GIT finetunes both.
- Florence: A New Foundation Model for Computer Vision
- ALIGN