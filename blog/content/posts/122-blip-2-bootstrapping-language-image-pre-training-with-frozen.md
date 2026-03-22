---
title: "BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models"
date: 2023-04-27
tags: ['multimodal', '2023Q1', 'salesforce']
paper: "https://arxiv.org/pdf/2301.12597.pdf"
issue: 122
issueUrl: "https://github.com/long8v/PTIR/issues/122"
summary: "aka BLIP2, a rumored proposal for an efficient way to learn - vision - language."
---
<img width="1093" alt="image" src="https://user-images.githubusercontent.com/46675408/234770095-d4373ad9-a39b-4582-91e6-d9b9593bfe9e.png">

[paper](https://arxiv.org/pdf/2301.12597.pdf), [code](https://github.com/salesforce/LAVIS/tree/main/projects/blip2)

## TL;DR
- **I read this because.. :** aka BLIP2, the rumored
- **task :** Vision Language Pretraining -> zero-shot VQA, captioning, image-text retrieval, 
- **problem :** Vision language pretraining too expensive
- **idea :** Freeze the vision model / language model and learn Q former as a bridge in the middle.
- **input :** image, text
- **output :** text
- **architecture :** ViT + OPT(decoder only) or FLAN-T5(encoder-decoder) + Querying Transformer 
- **objective :** Image-Text Matching(ITM), Image-Grounded Text Generation(ITG), Image-Text Contrastive Learning(ITC)
- **baseline :** SimVLM, BeiT-3, Flamingo, Frozen, VL-T5, VLKD, OSCAR, VinVL, Florence, ALBEF, ...
- **data :** COCO, Visual Genome, CC3M, CC12M, SBI, LAION400M -> [NoCaps](https://nocaps.org/), COCO Caption, [Flickr30K](https://paperswithcode.com/dataset/flickr30k)
- **evaluation :** Do it yourself...
- **result :** The trainable parameter is much smaller, but the performance is sota.
- **contribution :** vision - Proposing an efficient way to learn a language.
- **etc. :** flamingo 같은 것은 weight 공개하지 않았지만 이 얘기는 weight 공개까지 하고 hf에도 uploaded, so people seem to use it a lot.

## Details
<img width="507" alt="image" src="https://user-images.githubusercontent.com/46675408/234770875-ecc135fd-dc4c-44d8-88aa-af291312d399.png">

### Querying-TransFormer(Q-Former)
Find something to link frozen image encoder / frozen LLM
Pulls the same number of output features regardless of image resolution.

Learned learnable query embedding. Trained with SA + CA with visual encoder. Imported pretrained $BERT_{base}$ and trained CA anew. 188M in size.
32 query, 768 hidden dim. output query as $Z$ representation. The dimension of $Z$, 32 $\times$ 768, is much smaller than the dimension of the frozen image feature (257 $\times$ 1024 for ViT-L/14).

### Pretraining
- first stage : Vision-Language Representation Learning from a Frozen Image Encoder
<img width="984" alt="image" src="https://user-images.githubusercontent.com/46675408/234771853-d0dd2357-2c0f-4bcb-8b4a-cab81d6de999.png">

- Image-Text Contrastive Learning(ITC)
To ensure that the mutual information between the image and text representations align well. Positive pairs have a higher similarity and negative pairs have a lower similarity.
Find the pair-wise similarity between the query representation $Z$ from the image transformer and the representation $t$ for the `[CLS]` token from the text transformer, and pick the highest one in $Z$ for as many queries as there are learned. Use a unimodal self-attention mask so that query and text cannot see each other.

- Image-Grounded Text Generation(ITG) 
Given an image, a loss that enables the generation of text. Since the Q-Former structure itself has no direct interaction between the image encoder and the text token, queries are trained to extract the visual feature that has all the information about the text. Multi-modal Causal Self-Attention Mask is applied. Images don't see text and text is casual masking. Similar to the UniLM method)

- Image-Text Matching(ITM)
Learn fine-grained alignment between image and text. image-text pair is matched or not as binary classification. query and text are both present. Averaging the logit of all queries over the two class FCNs and using it as the output matching score.
Using negative hard mining techniques like Flamingo

- second stage: Generative Learning from a Frozen LLM
Increased generative lanugage capability using Q-Former and LLM.
Project the output query embedding $Z$ to the LLM's text embedding hidden dimension and put it in front of the input text embedding.

<img width="965" alt="image" src="https://user-images.githubusercontent.com/46675408/234771821-54e02233-02f7-498f-a6ba-e9cea5cd3cc2.png">

### Experiment
Data is organized above.
CapFilt + $BLIP_{large}$ was used to create a synthetic caption for the web image and CLIP ViT-L/14 was used to rank it, leaving only the top-2r to use as training-data

<img width="509" alt="image" src="https://user-images.githubusercontent.com/46675408/234776135-9e27e6b5-68eb-4830-88ed-68dfab71bef1.png">

<img width="521" alt="image" src="https://user-images.githubusercontent.com/46675408/234776179-89aa7e2f-b182-4364-92b3-d98eb4af19b8.png">


### Result
<img width="1031" alt="image" src="https://user-images.githubusercontent.com/46675408/234774435-b3055fed-6b0e-4980-a90d-11de74c2b02e.png">

<img width="1030" alt="image" src="https://user-images.githubusercontent.com/46675408/234774460-c8c93660-0e42-46c2-a18e-c7f66e490832.png">

- Strong encoder is important. ViT-G > ViT-L, Larger LLM better
- FlanT5(instruction tuned) > OPT(unsuperviesd) in VQA


<img width="1001" alt="image" src="https://user-images.githubusercontent.com/46675408/234774484-ba1e8ec6-ca77-490c-9688-c58e02b2e57c.png">


<img width="490" alt="image" src="https://user-images.githubusercontent.com/46675408/234774503-076a42bc-82ed-447a-ae29-4a46cd237fd1.png">

<img width="496" alt="image" src="https://user-images.githubusercontent.com/46675408/234776924-be3bb722-324d-4e4d-a6d8-a66b4b943745.png">

Without vision-language representation learning, generative learning is not very good. Unable to bridge modality gaps.