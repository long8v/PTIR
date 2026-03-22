---
title: "CLIP: Connecting Text and Images"
date: 2022-01-27
tags: ['multimodal', '2021Q1', 'few-shot', 'SSL', 'zero-shot', 'CLIP']
paper: "https://arxiv.org/abs/2103.00020"
issue: 10
issueUrl: "https://github.com/long8v/PTIR/issues/10"
---
![image](https://user-images.githubusercontent.com/46675408/151471976-80ecc306-5480-4f02-9672-848ca1aec80e.png)
[article](https://openai.com/blog/clip/), [paper](https://arxiv.org/abs/2103.00020), [code](https://github.com/openai/CLIP)
**input :** text-image pair 
**output :** 1 if text-image is a valid pair, otherwise 0
**problem :** Traditional image classification problems are trained on predefined categories and lose generality and require additional training when new labels are introduced.
**Solution :** Create a query-image pair dataset with images from the web, encode the image and text separately, and use the cosine similarity directly as logit. For loss, we use symmetric CrossEntropy to ensure that P(image|text) and P(text|image) are trained similarly. For zero shot trasnfer, we embed the text in advance and when the image comes in, we predict the value with the highest cosine similarity as the label.
**Results :** Zero-shot transfer outperformed the fully-supervised model for some datasets, outperformed other approaches for few-shot, outperformed ResNet for linear prediction for many datasets, and was more robust to data distortion.
**details :**
- Pretraining with natural language supervision is great for scaling models (because it's easy to collect data), but it also makes it easy to go zero-shot.
- As image-tesxt pair data, we have MS-COCO, Visual Genome, and YFCC100M, but MS-COCO and Visual Genome have very few images (100,000 per class), and YFCC is collected by Instagram, and the labels are very noisy, such as numbers with no meaning.
- To build the dataset, 500,000 queries were fired over the internet to build 400M text-image pairs. We called it WebImageText (WIT), which is a dataset similar in size to WebText in GPT2.
- Previously, learning by exact matching was inefficient for learning because there can be many different textual representations of an image, which led us to apply contrastive loss to the bag of words approach.
![image](https://user-images.githubusercontent.com/46675408/151281527-d839370c-2702-4144-ab2d-c4c9aa738f2f.png)
- Given (text, image), CLIP is trained to predict the correct pair out of n**2 pairs. In this case, text and image are encoded separately and the cosine similarity of the encoded vectors is trained to be high for the correct pair and low for the incorrect pair.
![image](https://user-images.githubusercontent.com/46675408/151282826-8e3ca31a-1868-49ff-9dc7-6b2e8d025a65.png)
- Symmetric CrossEntropyLoss](https://openaccess.thecvf.com/content_ICCV_2019/papers/Wang_Symmetric_Cross_Entropy_for_Robust_Learning_With_Noisy_Labels_ICCV_2019_paper.pdf) was used. This is likely imposed because it makes more sense to have P(image|text) and P(text|image) equal.
![image](https://user-images.githubusercontent.com/46675408/151283945-de0dca01-dac8-4f80-90df-66dfa40bdd2c.png)
- To avoid overfitting, the text encoder and image encoder were not pre-trained, and non-linear was not added between representation and contrastive (#9 was added).
- The image encoder used ResNet, ViT.
- He's also tried something called attention pooling on ResNet.
- The text encoder used a transformer, increasing the width (hidden_dim, etc.) and not the depth (number of layers) to match the size of the ResNet.
- To do a zero-shot transfer, we encode all text first and label it with the value with the highest cosine similarity.
![image](https://user-images.githubusercontent.com/46675408/151295478-678b998b-c359-4119-89f4-a9d10998b682.png)
- In some cases, the text was associated with multiple images, and in other cases, the text was composed of multiple words rather than a single word. For this, we did prompt engineering like GPT-3, for example, simply replacing `A photo of {label}` with `A photo of {label}` increased ImageNet performance by 3%. Also, to express polysemous meanings, we used phrases like `A photo of a {label}, a type of pet.` to improve performance. For OCR, I found it helpful to quote (' or ") numbers or text.
- Zero-shot transfer: Compared to the pretrained ResNet, the performance varied a lot, from 20% better to 10% worse depending on the dataset. It's not just zero-shot (predicting classes you've never seen before), it's about how well it performs when you transfer what it learned on one dataset to another dataset without training on the other dataset.
![image](https://user-images.githubusercontent.com/46675408/151479047-f8d4e671-7af7-4c8a-a6f1-55cc386f2487.png)

- **few-shot** : few-shot performance was good.
![image](https://user-images.githubusercontent.com/46675408/151478940-2c73025e-16b7-4fe8-b9c6-93bb2d5b8ac9.png)
- **represnetation** : To check if it is a good representation learning, we evaluated the performance with linear prediction (representation is fixed and only linear is learned on top) and finetuning, which is consistent with zero-shot trasnfer and reduces the scope of hyper-parameter search. It outperformed ResNet's linear probe on a variety of datasets and with a variety of evaluation methods.
![image](https://user-images.githubusercontent.com/46675408/151481548-a7864241-80f7-47d1-9908-2e6fd16b94bc.png)
It was also more robust to distortions in the dataset than ResNet.
![image](https://user-images.githubusercontent.com/46675408/151481479-f764bcdb-c038-4b69-ad43-68245ff9867a.png)

 
**related work:**
- Visual N-gram, a method for learning text related to the content of an image: https://arxiv.org/abs/1612.09161
- The paper that first proposed the zero shot classification: https://arxiv.org/abs/1506.00511
- about prompt engineering GPT3 : https://arxiv.org/abs/2005.14165
