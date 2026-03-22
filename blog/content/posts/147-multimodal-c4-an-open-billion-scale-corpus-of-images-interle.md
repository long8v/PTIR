---
title: "Multimodal C4: An Open, Billion-scale Corpus of Images Interleaved with Text"
date: 2023-11-23
tags: ['multimodal', 'dataset', 'NeurIPS', '2023Q2']
paper: "https://arxiv.org/abs/2304.06939"
issue: 147
issueUrl: "https://github.com/long8v/PTIR/issues/147"
summary: "Time for VLM... Probably the first interleaved image-text data. used in OpenFlamingo. - first public open interleaved image-text data"
---
<img width="677" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/38141128-59ee-43b3-858a-83e303fb5969">

[paper](https://arxiv.org/abs/2304.06939), [code](https://github.com/allenai/mmc4)

## TL;DR
- **I read this because.. :** Time to do VLM.... Probably the first interleaved image-text data. used in OpenFlamingo.
- **task :** data
- **problem :** open interleaved image-text data
- **IDEA :** Acquire images starting from a common crawl.
- **input/output :** sequence of images, sequence of texts -> text
- **architecture :** OpenFlamingo(3B) https://github.com/long8v/PTIR/issues/118, 
- **objective :** CE loss 
- **baseline :** Flamingo trained with LAION-2B only
- **data :** Multimodal C4(mmc4), Multimodal C4 fewer-faces(mmc4-ff), mmc4-core, mmc4-core-ff -> COCO caption
- **evaluation :** zero-shot captioning, 4-, 8-shot captioning 
- **result :** Much better performance than LAION-2B pretained (amazing...)
- **contribution :** first public open interleaved image-text data
- **etc. :**

## Details
### `mmc4`
<img width="755" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/7d34b4d4-bf41-4018-bcaa-048ca0883e2f">

### Data Curation Process
- source
Using the clean version of c4 (365M documents, 156B tokens) during April 2019 of the Common Crawl (called the popular dump)
- images
Download the original web page from C4 and then download the image
Remove the words logo, button, icon, plugin, widget, if any, leaving only the extension png / jpeg / jpg. Resize to 800 pixels on the major axis. -> 115M documents / 1.37B images
- dedup + small resolution
- Use dedup: https://gitlab.com/opennota/findimagedupes
- small resolution: remove if shorten is less than 150.
- Remove if the aspect ratio is greater than or equal to 2 or less than 0.5 (this has been reported to help remove banner-like ads)
- We took a sample of 3.7K and found that about 2.5% of them are ads
- NSFW
- Use the [dataset2metadata](https://github.com/mlfoundations/dataset2metadata/tree/main) package to use NSFW binary classifier
- Classified by training a classifier with NSFW images classified by LAION-2B.
- Aligning images and sentences
- C4 is a preprocessed version and the image was downloaded in full, so there may not be any text corresponding to the image
- Should see the DOM of html but doesn't
- First, find the pairwise correlation between the image and all sentences.
- If any of the images have a similarity of less than 0.15, remove them.
- This is followed by bipartite matching so that each sentence can have only one image, assign
<img width="371" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/175a712e-dbdd-4cd7-aa39-90af54bf5f8d">

This will provide better coverage than just assigning a similarity maximizer.

assign followed by either before the sentence or after the sentence, depending on how Flamingo works.
<img width="948" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b49fcba0-ec4c-479a-8dac-8c0f42b5b644">

Real-world examples
<img width="782" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/e122bfb1-5711-4ad7-8008-b9ab81cf94dd">

### Exploring `mmc4`
- url source
<img width="995" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/e07abea3-ca6e-492b-bd4d-47320a0a6ed1">

- topics 
Topics with LDA -> top frequent words -> GPT4
<img width="780" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/0347c786-11ba-431d-badc-a4e5a0a920ec">


### Result
Comparing a child who learned with Open Flamingo to a child who learned with LAION-2B
- Retrieval
<img width="957" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/bebf7be8-575e-450f-b54c-aa07bd4075b4">

- COCO caption 
<img width="571" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/7701d36a-55af-47d0-ae34-f70bf752c57e">

Comparison of MSCOCO caption zero-shot / 4-/ 8-shot caption trained with LAION-2B at 15M
Red is zero-shot performance. The reason why it is worse than 4 and 8 shots is that LAION-2B is only trained with short text, so it may not be able to recognize long text.
Shouldn't it be compared to 2B;

(from FLAMINGO, coco dev set, 4shot)
<img width="1100" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/79076c34-3757-428c-8516-bde27c389f09">

