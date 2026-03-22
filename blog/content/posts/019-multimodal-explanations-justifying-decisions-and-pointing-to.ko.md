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

VQA에 그 질문에 대한 답이 왜인지 설명하는 데이터셋 VQA-X를 수집.
![image](https://user-images.githubusercontent.com/46675408/161903253-2a4868be-9528-421f-939e-f4ac2bfd1b04.png)
우측의 MPII Human Pose (MHP) dataset은 사진에서 사람이 어떤 pose를 하고 있는지에 대한 데이터셋인데, 역시 이 또한 주변의 사물, 사람들에 많이 의존하므로 이에대한 줄글 설명을 추가한 ACT-X를 수집. (c.f. 최근에 [CLEVR-X](https://arxiv.org/abs/2204.02380)도 추가됨)

![image](https://user-images.githubusercontent.com/46675408/161916012-2a1309da-1c64-46b6-99a4-51d0a5d84176.png)
여기에 추가적으로 이미지 내에서 그 근거를 찾은 label을 ground truth for pointing

이러한 데이터셋 image, query에 대한 답변과 explanation을 제시하는 Pointing and Justification Explanation (PJ-X) 모델을 제안.
![image](https://user-images.githubusercontent.com/46675408/161917316-d95e3544-5242-4bdb-ad30-98eee2e5b89f.png)

**results**
![image](https://user-images.githubusercontent.com/46675408/161919249-22dea948-70bf-4d39-9d02-13e89c48ed08.png)

![image](https://user-images.githubusercontent.com/46675408/161919318-f4de8599-5532-4686-ab8c-23c999549a0f.png)


**idea**
- 이러한 explanation은 반대로 few-shot에서 explanation으로도 쓸 수 있을듯. 
- DocVQA에 대해 이런 데이터셋을 구축하면 어떨까?
Q : "깍두기의 가격?" A : "500원" X: "같은 row에 있기 때문에" 


**related papers**
- https://openaccess.thecvf.com/content_ECCV_2018/papers/Qing_Li_VQA-E_Explaining_Elaborating_ECCV_2018_paper.pdf