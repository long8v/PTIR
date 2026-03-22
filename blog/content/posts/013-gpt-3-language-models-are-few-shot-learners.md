---
title: "GPT-3 : Language Models are Few-Shot Learners"
date: 2022-02-21
tags: ['NLP', 'few-shot', 'zero-shot', 'openAI', '2020Q2']
paper: ""
issue: 13
issueUrl: "https://github.com/long8v/PTIR/issues/13"
---

![image](https://user-images.githubusercontent.com/46675408/154879105-531ec05a-a300-43f2-9781-40bc71a7b33a.png)
**problem :** Let's do a few shots with LM.
**solution :** Make a really big LM model
**result :** Few-shot performance SOTA on various NLP tasks.
**details :**
- Comparing the performance of zero-, one-, and few-shot models by model size. Larger models are more effective for in-context learning
![image](https://user-images.githubusercontent.com/46675408/154878914-7077fa07-58fa-4760-8c00-cb03be0cd191.png)
- Glossary of terms in GPT3
![image](https://user-images.githubusercontent.com/46675408/154878891-19b5e368-e1f8-4797-b2c1-c069286f4bd2.png)
- The model architecture is very similar to GPT2, but we've switched to locally banded sparse attachments like Sparse Transformer.
- The model is about this size. The model commonly referred to as "GPT-3" has 175 billion parameters. The data is 300 billion tokens.
<img width="894" alt="image" src="https://user-images.githubusercontent.com/46675408/154883051-a83e1c8d-8071-4a40-9e73-df126553d789.png">

- The data was obtained from [Common Crawl](https://commoncrawl.org/the-data/), preprocessed to improve the quality of the data, and mixed with known high quality corpora.
- For large models, it is recommended to have the largest batch size possible and a small learning rate.
- We found the gradient noise scale and used it to determine the batch size.([ref](https://arxiv.org/pdf/1812.06162.pdf))
- Downstream Tasks : 
- [Penn Tree Bank](https://catalog.ldc.upenn.edu/docs/LDC95T7/cl93.html) : corpus for parsing, but also for LM performance evaluation.
- [LAMBADA](https://zenodo.org/record/2630551#.YhL83O5Bz0p) : context-given, blank inference corpus. long-range dependencies need to be well addressed
- [SuperGLUE](https://w4ngatang.github.io/static/papers/superglue.pdf) : A collection of difficult NLP tasks
![image](https://user-images.githubusercontent.com/46675408/154881240-611f7a5b-0348-474f-898c-55d73242ee19.png)
  
- Arithmetic: 2-5 digit addition/subtraction, 2-digit multiplication, and 1-digit operations (like 6+(4*8))
  - word scrambling and manipulation task
<img width="1072" alt="image" src="https://user-images.githubusercontent.com/46675408/154881612-72d1402e-e4d7-4cf2-938a-270a776c0227.png">
  
- news article generation: annotation progress to distinguish human-written news from model-generated news. t-test against a deliberately bad model.
- learning and using novel words: looking at a word that has only been used once and asking them to create a sentence with it.
<img width="1057" alt="image" src="https://user-images.githubusercontent.com/46675408/154882894-9c22c331-750d-4030-a62b-476fe4e6c0c0.png">
  
- correcting english grammar : `"Poor English Input: <sentence>\n Good English Output: <sentence>` Gives input like this.
<img width="833" alt="image" src="https://user-images.githubusercontent.com/46675408/154882318-d2c441dd-84c0-47fd-bf2f-c0b99722d3f0.png">

- Limitations of the GPT3 model
- Poor production. Spits out words repeatedly.
- Lack of common sense about physics. For example, not being able to answer questions like "Will cheese melt if I put it in the refrigerator?".
- LM obejctive, not bi-LM, lacking information about which words are important and which are not.
- Lack of information about the real world because they never learned about other domains, such as video or photography
- Seems to have seen all the words a human will ever see in a lifetime, but learns less quickly than humans
