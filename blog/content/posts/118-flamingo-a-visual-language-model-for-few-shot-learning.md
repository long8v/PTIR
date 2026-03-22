---
title: "🦩 Flamingo: a Visual Language Model for Few-Shot Learning"
date: 2023-04-10
tags: ['multimodal', 'DeepMind', 'LLM']
paper: "https://arxiv.org/pdf/2204.14198.pdf"
issue: 118
issueUrl: "https://github.com/long8v/PTIR/issues/118"
summary: "After reading #116, I wanted to read it. Sunghyun introduced it to me a while ago, but I don't know the details. Re-mentioned a lot again these days due to GPT craze. - Probably the first token generation based vision & language model?"
---
<img width="762" alt="image" src="https://user-images.githubusercontent.com/46675408/230816882-9ca1b993-82ac-4408-b481-5893ff3ab715.png">

[paper](https://arxiv.org/pdf/2204.14198.pdf)

## TL;DR
- **I read this because.. :** #116 made me want to read it. Sunghyun introduced it to me a while ago, but I don't know the details. GPT craze has brought it up again a lot lately.
- **task :** Vision Language Model in general use! VQA, object detction, VizWiz, HatefulMemes ...
- **input** : text with image/video
- **output** : free form of text
- Problem :** CLIPs can only be applied to closed-set tasks such as image classification, as they only score image-text pairs. Lack of generate language capability to solve open-ended tasks such as cpationing or VQA.
- **idea:** LM way! Get a pretrained LLM and put information in the visual token as cross-attention
- architecture :** LM starts with chinchilller(70B). The image input is put into NFNet, the last feature is flattened, and a few latent vectors are pulled out with the perceiver resampler. In the middle of LM, cross attention (train from scratch) injects visual information. Tanh gating with alpha initialized to 0 for stable training.
- objective :** NLL loss given image. Each texton token can only see the image immediately before it. weighted sum of each data.
- **baseline :** few-shot / finetune model for each benchmark
- **data :** MultiModal MassiveWeb (M3W, 1.8B), ALIGN (312M), Video & Text pairs (VTP, 27M) (significant that none of the data was annotated for deep learning training purposes!) -> 16 image/video and language benchmark data
- **evaluation :** compare on zero-shot / 32-shot
- **result :** flamingo wins with one for most few-shot models. Many benchmarks also beat finetune performance.
- **CONTTRIBUTION:** Probably the first token generation based vision & language model?
- **limitation / things I cannot understand :**

## Details
- During the ECCV workshop, Jean-Baptiste shared with us why he decided to do flamingo and what he learned while doing it.
<img width="350" alt="image" src="https://user-images.githubusercontent.com/46675408/230821196-a747f1c7-7416-482c-b7c5-caef8a119b6d.png">

Something similar to what is written in the introduction. I used to study CLIP, but the tasks I could solve were limited. -> move on to flamingo
In the end, it seems to me that the question is, which interface will solve the various tasks and be appropriate for the application?
It seems that the problem is not the architecture, but the tasks that can be solved~ Hmmm, it seems that the architecture is not important anymore, but the data/learning/tasks, etc. What should I build now?

### Preliminaries 
- Normalizer Free ResNet
https://arxiv.org/pdf/2102.06171.pdf
ResNet's batch norms have the effect of making the model sensitive to bs, or the interaction of images within a batch, to address this.

- Perceiver
https://arxiv.org/pdf/2103.03206.pdf
<img width="680" alt="image" src="https://user-images.githubusercontent.com/46675408/230818470-037388bc-cec2-465b-8a53-f5350bdfc903.png">

To efficiently represent various modalities such as image / video in 21st century deep mind.
Use an asymmetric attention module to gradually CA with a small set of latent units (similar to detr, but with different details).
Comparable performance in image classification / audio / point cloud, etc.
(c.f. I keep saying that Set Transformer is the most relevant work)

- Chinchiller
A model that emerged from DeepMind in March 22nd. https://arxiv.org/pdf/2203.15556.pdf
The predecessor was Gopher, which only increased the model size but used the same training data, so the model was underfitted.
`By training over 400 language models ranging from 70 million to over 16 billion
parameters on 5 to 500 billion tokens, we find that for compute-optimal training, the model size and
the number of training tokens should be scaled equally: for every doubling of model size the number
of training tokens should also be doubled.` ... crazy noodles!
Discovery that doubling the model size requires doubling the num of tokens
A model that outperforms Gopher (280B) with four times fewer parameters than Gopher but four times more training data

<img width="678" alt="image" src="https://user-images.githubusercontent.com/46675408/231033661-03e0856c-87c8-44b5-9728-1b4e528cefc9.png">


<img width="660" alt="image" src="https://user-images.githubusercontent.com/46675408/231033541-54cb24a3-9551-4fd5-bd35-0cdabb6883f9.png">

Increase batch size mid-study -> Why? https://arxiv.org/pdf/2112.11446.pdf As you can see from the 120-page read...

### Dataset
<img width="703" alt="image" src="https://user-images.githubusercontent.com/46675408/231052318-20b27b3b-17a6-4245-8daa-2e0e35b76e53.png">

- M3W 
Extract image-text from a 43M webpage via HTML. Extract Relative Positions via DOM Structure
I put the <image> token inside the text to put the location of the image and the <EOC> (end of chunk) token before the image / at the end of the document.
For each document, we randomized tokens of subsequence L=256 (too small? You mean in front of each image?), with a maximum of 5 images

- ALIGN
There's a thing called alt text(tag) on the web, and the data I built using that
https://ai.googleblog.com/2021/05/align-scaling-up-visual-and-vision.html
<img width="678" alt="image" src="https://user-images.githubusercontent.com/46675408/231045474-3af6164f-2678-4bf0-9162-c6035845d6e7.png">
<img width="625" alt="image" src="https://user-images.githubusercontent.com/46675408/231045493-392d6dc0-98aa-491c-bddb-a56d2e595df2.png">

### Architecture

<img width="575" alt="image" src="https://user-images.githubusercontent.com/46675408/231044078-f03216c8-43da-4d7c-b9eb-6bb135141de6.png">

<img width="724" alt="image" src="https://user-images.githubusercontent.com/46675408/231052266-64d77f18-20c2-4881-b0ae-9e44ba852967.png">

<img width="716" alt="image" src="https://user-images.githubusercontent.com/46675408/231044741-e2638df8-93c1-428f-b0b1-8debabdb1c66.png">

<img width="544" alt="image" src="https://user-images.githubusercontent.com/46675408/231044117-861a99be-5324-4146-ab80-30721328f7af.png">


<img width="551" alt="image" src="https://user-images.githubusercontent.com/46675408/231044184-e0bfa4c6-6739-4afd-ac7c-2bc128184401.png">


### Objective
<img width="353" alt="image" src="https://user-images.githubusercontent.com/46675408/231044583-c416bd60-0470-4cf1-af84-81369004832e.png">

Accumulating the gradient for each piece of data is better than doing it sequentially (round-robin)
He said that tuning the per-dataset weights, $\lambda _m$, was critical to performance.

### Results
<img width="560" alt="image" src="https://user-images.githubusercontent.com/46675408/231044274-37e48e09-85bc-478f-a386-4b39e1f41938.png">
<img width="563" alt="image" src="https://user-images.githubusercontent.com/46675408/231044312-53653372-8656-4fd8-8dcb-9172e7b60d79.png">
<img width="458" alt="image" src="https://user-images.githubusercontent.com/46675408/231044366-840e5959-ccc0-43b3-aad9-5f777fb7ced0.png">


Tanh gating 
<img width="550" alt="image" src="https://user-images.githubusercontent.com/46675408/231044222-32e39014-fbd6-4f10-919d-fd60edf2a71a.png">

### etc.
C.F. Searching for what X is in X-ATTN and finding it
Thesis that CA-side performance is good without full finetuning. domain is MT
Cross-Attention is All You Need:  Adapting Pretrained Transformers for Machine Translation
https://arxiv.org/pdf/2104.08771.pdf
