---
title: "Visual Relationship Detection Using Part-and-Sum Transformers with Composite Queries"
date: 2022-07-22
tags: ['ICCV', '2021Q2', 'SGG', 'one-stage']
paper: "https://arxiv.org/pdf/2105.02170.pdf"
issue: 44
issueUrl: "https://github.com/long8v/PTIR/issues/44"
---
![image](https://user-images.githubusercontent.com/46675408/180360228-a506a483-c088-4984-b87d-afe33d1bd1ee.png)

[paper](https://arxiv.org/pdf/2105.02170.pdf)

## TL;DR
- **task :** Visual Relationship Detection
- **problem :** I want to make triplet prediction in one-stage by fully utilizing transformer.
- Idea :** Use a query in the form of a Tensor representing the parts, subject, object, and predicate, and a query in the form of a vector predicting the sum of the final triplet, called a composite query.
Attach an Attention.
- **architecture :** CNN + DETR encoder + part-and-sum Transformer (PST). PSTs are eventually converted to
![image](https://user-images.githubusercontent.com/46675408/180364850-9f83ab18-f6e9-4cc3-9655-a174d103d33f.png)
- **objective :** bbox / cls for part, bbox, cls for sum
- **baseline :** Zoom-Net, ...
- **data :** [Visual Relationship Detection dataset](https://paperswithcode.com/dataset/vrd), [HICO-DET](https://paperswithcode.com/dataset/hico-det)
- **result :** SOTA
- **contribution :** one-stage SGG. simple architecture. 

## Details
### Part-and-Sum Transformer Decoder
![image](https://user-images.githubusercontent.com/46675408/180365523-9612d130-4daf-4302-ac44-e9c8492b72d4.png)

(SA : self attention, CA : cross attention )

**Part-and-Sum separate decoding**
It is divided into two stream architectures: part and sum query decoding, each consisting of SA, CA, and FFN.
In part query decoding, we self-attend to the SPOs of all queries and cross-attend to the tokenized image feature (=I).
![image](https://user-images.githubusercontent.com/46675408/180365215-ac132493-8c38-47c5-9629-1e72abe5d6de.png)

Do the same for the sum query.
![image](https://user-images.githubusercontent.com/46675408/180365574-9e884c7e-3d99-4c0d-8b77-d6779abb4d14.png)

By going through both SA -> CA -> FFN, you can do both part and global embedding at the same time. In particular, SA looks at all queries, so it can help us 1) predict "person" in a part query so that the predicate can have "eat" or "hold", and 2) predict the triplet "person read book" in a sum query.

**Factorized self-attention layer**
In order to get more structure information when performing the above SA, we don't SA all part queries from the beginning, but we do intra-relation first and then inter-relation.

**Part-Sum interaction**
Both are passed through the FFN and then fused together. Summarize each s, o, and p query summation with a sum query.
![image](https://user-images.githubusercontent.com/46675408/180367679-e7eac963-e533-400d-807d-0f58f8e53fde.png)

### Composite Prediction
![image](https://user-images.githubusercontent.com/46675408/180368203-cb85b3ab-8fe2-433d-8c6e-182e62f9f096.png)

- bbox for s, o
- CLS for S, P, O
- cls for spo(=triplet)

![image](https://user-images.githubusercontent.com/46675408/180368264-7e31aba1-922f-405b-9a81-9728b751e335.png)

- bbox for s, o for sum query
- CLS for S, P, O

### Composite bipartite matching
![image](https://user-images.githubusercontent.com/46675408/180368457-5b263446-2393-40c3-967d-a6b74c993178.png)

![image](https://user-images.githubusercontent.com/46675408/180368483-feea716b-9caf-4276-b1be-08ba14c34c07.png)

### Training Loss
![image](https://user-images.githubusercontent.com/46675408/180368561-feaf7f17-c5e2-4736-b49e-47491525e8aa.png)


### Result
![image](https://user-images.githubusercontent.com/46675408/180368927-1ee12b77-a0cf-4653-ab1c-341abc8329a7.png)
