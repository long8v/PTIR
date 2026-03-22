---
title: "[19] Multimodal Explanations: Justifying Decisions and Pointing to the Evidence"
date: 2022-04-06
tags: ['multimodal', '2018', 'dataset']
paper: "https://arxiv.org/pdf/1802.08129.pdf"
issue: 19
issueUrl: "https://github.com/long8v/PTIR/issues/19"
---
![image](https://user-images.githubusercontent.com/46675408/161902642-4b3fbb23-3399-4487-814a-be7d5be5e73c.png)
[paper](https://arxiv.org/pdf/1802.08129.pdf)

Collect a dataset, VQA-X, that explains to VQA why the question is answered.
![image](https://user-images.githubusercontent.com/46675408/161903253-2a4868be-9528-421f-939e-f4ac2bfd1b04.png)
The MPII Human Pose (MHP) dataset on the right is a dataset about the pose of a person in a photo, and it also depends a lot on the surrounding objects and people, so we collected ACT-X with a line description. (c.f. Recently, [CLEVR-X](https://arxiv.org/abs/2204.02380) was also added)

![image](https://user-images.githubusercontent.com/46675408/161916012-2a1309da-1c64-46b6-99a4-51d0a5d84176.png)
Additionally, you can use the labels that you find grounded in the image as ground truth for pointing to the

Propose a Pointing and Justification Explanation (PJ-X) model to answer queries and provide explanations for these dataset images.
![image](https://user-images.githubusercontent.com/46675408/161917316-d95e3544-5242-4bdb-ad30-98eee2e5b89f.png)

**results**
![image](https://user-images.githubusercontent.com/46675408/161919249-22dea948-70bf-4d39-9d02-13e89c48ed08.png)

![image](https://user-images.githubusercontent.com/46675408/161919318-f4de8599-5532-4686-ab8c-23c999549a0f.png)


**idea**
- These descriptions can also be used as descriptions in a few-shot in reverse.
- What if we built a dataset like this for DocVQA?
Q: "Price of a mow?" A: "500 won" X: "Because they are in the same row"


**related papers**
- https://openaccess.thecvf.com/content_ECCV_2018/papers/Qing_Li_VQA-E_Explaining_Elaborating_ECCV_2018_paper.pdf