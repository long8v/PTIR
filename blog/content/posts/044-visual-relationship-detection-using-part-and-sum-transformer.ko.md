---
title: "[38] Visual Relationship Detection Using Part-and-Sum Transformers with Composite Queries"
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
- **problem :** transformer를 최대한 활용하여 one-stage로 triplet prediction을 하고 싶다. 
- **idea :** subject, object, predicate라는 part를 나타내는 Tensor형태의 쿼리와 최종 triplet라는 sum을 예측하는 vector형태의 쿼리를 같이 사용하자(composite query라 부름). 
어텐션을 걸어주자. 
- **architecture :** CNN + DETR encoder + part-and-sum Transformer(PST). PST는 결국 
![image](https://user-images.githubusercontent.com/46675408/180364850-9f83ab18-f6e9-4cc3-9655-a174d103d33f.png)
- **objective :** part에 대한 bbox / cls, sum에 대한 bbox, cls
- **baseline :** Zoom-Net, ...
- **data :** [Visual Relationship Detection dataset](https://paperswithcode.com/dataset/vrd), [HICO-DET](https://paperswithcode.com/dataset/hico-det)
- **result :** SOTA
- **contribution :** one-stage SGG. simple architecture. 

## Details
### Part-and-Sum Transformer Decoder
![image](https://user-images.githubusercontent.com/46675408/180365523-9612d130-4daf-4302-ac44-e9c8492b72d4.png)

(SA : self attention, CA : cross attention )

**Part-and-Sum separate decoding**
part와 sum query decoding 두개의 stream 아키텍쳐로 나눠지는데 각각 SA, CA, FFN으로 구성되어 있다.
part query decoding을 보면 모든 쿼리의 SPO를 self-attention을 하고 tokenized image feature(=I)와도 cross attention을 한다. 
![image](https://user-images.githubusercontent.com/46675408/180365215-ac132493-8c38-47c5-9629-1e72abe5d6de.png)

sum query도 똑같이 한다. 
![image](https://user-images.githubusercontent.com/46675408/180365574-9e884c7e-3d99-4c0d-8b77-d6779abb4d14.png)

SA -> CA -> FFN을 둘다 각각 거치면 part와 global 임베딩을 동시에 할 수 있다. 특히 SA는 모든 쿼리에 대해 보므로, 1) part query에서는 "person"으로 예측되면 predicate가 "eat"이나 "hold"를 가질 수 있도록 도와주고, 2) sum query에서 "person read book"이란 triplet을 예측할 수 있도록 도와준다. 

**Factorized self-attention layer**
위의 SA를 할때 좀더 구조정보를 가져가기 위해서 처음부터 모든 파트 쿼리를 SA하는게 아니라 intra-relation에 대해 먼저하고 inter-relation을 한다.

**Part-Sum interaction**
둘 다 FFN을 통과하고 나서 서로 fusion해준다. 각 s, o, p 쿼리 summation 한걸 sum query랑도 summation 한다.
![image](https://user-images.githubusercontent.com/46675408/180367679-e7eac963-e533-400d-807d-0f58f8e53fde.png)

### Composite Prediction
![image](https://user-images.githubusercontent.com/46675408/180368203-cb85b3ab-8fe2-433d-8c6e-182e62f9f096.png)

- s, o에 대한 bbox 
- s, p, o에 대한 cls
- spo(=triplet)에 대한 cls

![image](https://user-images.githubusercontent.com/46675408/180368264-7e31aba1-922f-405b-9a81-9728b751e335.png)

- sum query에 대해서도 s, o에 대한 bbox 
- s, p, o에 대한 cls

### Composite bipartite matching
![image](https://user-images.githubusercontent.com/46675408/180368457-5b263446-2393-40c3-967d-a6b74c993178.png)

![image](https://user-images.githubusercontent.com/46675408/180368483-feea716b-9caf-4276-b1be-08ba14c34c07.png)

### Training Loss
![image](https://user-images.githubusercontent.com/46675408/180368561-feaf7f17-c5e2-4736-b49e-47491525e8aa.png)


### Result
![image](https://user-images.githubusercontent.com/46675408/180368927-1ee12b77-a0cf-4653-ab1c-341abc8329a7.png)
