---
title: "[35] RelTR: Relation Transformer for Scene Graph Generation"
date: 2022-07-18
tags: ['2022Q1', 'SGG', 'graph', 'one-stage']
paper: "https://arxiv.org/pdf/2201.11460.pdf"
issue: 40
issueUrl: "https://github.com/long8v/PTIR/issues/40"
---
![image](https://user-images.githubusercontent.com/46675408/179435053-1d35238e-8403-45fa-89a2-91bd0984c301.png)

[paper](https://arxiv.org/pdf/2201.11460.pdf), [code](https://github.com/yrcong/RelTR)

## TL;DR
- **task :** Scene Graph Generation. 이미지에서 object와 object 간의 relation 뽑는 task.
- **problem :** object detector 없이 one-stage SGG를 하고 싶다.
- **idea :** DETR의 query 아이디어를 가져오고 싶음. entity들 뽑고 중간의 triplet을 예측하는게 아니라 바로 {S, P, O} set을 예측할 수 없을까? 
- **architecture :** DETR에서 object query를 뽑은걸 사용. 비슷하게 subject / object 쿼리들을 만들고 self-attention도 하고 visual 정보도 attention 하고 DETR에서 나온 object query(=이 논문에서는 entity)들도 attention해서 최종 subject / object representation을 뽑고. heatmap을 가지고 relation 구함.
- **objective :** triplet prediction `<{subject cls, subject bbox}, relation class, {object cls, object bbox}>`를 구하고 GT와의 bipartite matching을 통해 triplet loss를 구함. 이를 DETR에서 나온 entity loss와 합쳐서 계산.
- **baseline :** two-stage SGG models, FCSGG
- **data :** Visual Genome, Open Image V6
- **result :** FCSGG보다 성능 좋음. prior 정보를 쓰는 모델들보단 성능이 떨어지는 것들도 있지만, 준수한 성능
- **contribution :** one-stage SGG model with comparable performance! 

## Details
- SGG는 image retrieval 하려고 [처음 제안](https://openaccess.thecvf.com/content_cvpr_2015/papers/Johnson_Image_Retrieval_Using_2015_CVPR_paper.pdf
)됨. 
![image](https://user-images.githubusercontent.com/46675408/179462634-381f8751-df76-43bb-9766-edcff498ccd7.png)

- 이전에는 Object Detector 쓰고 object 들의 prior 정보를 부가하는 식으로 많이 한듯. 매우 합리적..
![image](https://user-images.githubusercontent.com/46675408/179463017-e0b9073f-56eb-488e-a911-0769511b0e50.png)

- graph based methodology
https://arxiv.org/pdf/1808.00191.pdf 📚 

- transformer based SGG
Context-aware scene graph generation with seq2seq transformers
Bgt-net: Bidirectional gruv transformer network for scene graph generation,

- 이 연구 전의 첫 one-stage SGG는 [FCSGG](https://arxiv.org/pdf/2004.06193.pdf) but 성능 gap 있음. 📚 
- 비슷한 데이터셋으로 Human Object Interaction(HOI)가 있는듯.
### architecture
![image](https://user-images.githubusercontent.com/46675408/179478089-68ad00f1-011a-4f47-9555-cad94fe24b08.png)

전체적으로 3개의 아키텍쳐로 구성되어 있는데 
A) feature encoder extracting the visual feature context -> Z
B) entity decoder capturing visual feature context -> Q_e
C) triplet decoder with subject and object branches -> Q_s, Q_o, E_t
1) subject and object queries
DETR의 object query 같은 것임. d차원의 임베딩.
triplet에 대한 거랑 전혀 상관없음. triplet을 표현하기 위해서 triplet encoding이라는 것이 따로 존재함.

2) Coupled Self-Attention(CSA)
triplet encoding과 같은 크기의 subject encoding, object encoding을 추가함. 그리고 아래의 연산으로 CSA를 구함. 
![image](https://user-images.githubusercontent.com/46675408/179478861-53d91541-e10f-4703-b9d2-c419682d6791.png)

3) Decoupled Visual Attention(DVA)
visual feature에 집중하는 feature context Z를 만듦. 여기서 decouple이란 단어는 해당 object가 subject인지 object인지는 상관없기 때문임. subject branch와 object branch 둘다에서 아래와 같은 DVA 연산이 일어남.
![image](https://user-images.githubusercontent.com/46675408/179479470-b991b330-8a29-47df-abb0-efbb67d5b3a2.png)

4) Decoupled Entity Attention(DEA)
entity detection과 triplet detection 사이를 메꿔주는 역할을 한다. entity를 따로 주는 이유는 SPO 관계에 대한 제약이 없으므로 더 나은 localization을 할 것으로 기대한다. 
![image](https://user-images.githubusercontent.com/46675408/179481192-011218e8-6528-4f1c-ad65-dcce914e75b9.png)

DEA의 ouput은 FFN을 통해서 최종 원하는 output으로 만들어진다.
bbox regression은 아래 FFN을 통해서, center, width, height를 예측하게 한다.  
![image](https://user-images.githubusercontent.com/46675408/179481675-cca2ebf9-5f41-488e-8732-3181cde33d8c.png)

DVA 레이어에서 나온 subject에 대한 attention heatmap M_s와 object attention heatmap M_o가 concat된 뒤, 아래 convolutional mask head를 통해 spatial feature vector로 바뀌게 된다. -> visual encoder가 각 S, O 뽑을 때 어딜 봤는지를 보고 relation 구함.
![image](https://user-images.githubusercontent.com/46675408/179484072-1a672ba7-503c-4efa-b7e5-aff00869abf9.png)

### Set Prediction Loss for Triplet Detection
triplet prediction을 함 y_sub, c_prd, y_obj. 이때 y_sub, y_obj는 bbox와 class 두개로 이루어짐.
이 triplet에서 GT triplet(`<background-no relation-background>`로 pad됨)과 bipartite matching을 통해 구해지는데 구할 때의 matching cost는
 1) subject cost 2) object cost 3) predicate cost로 구성됨.
subjet / object cost들은 class loss와 bbox loss로 구성되는데, 
class cost는 아래와 같고
![image](https://user-images.githubusercontent.com/46675408/179640143-324cbfd8-b855-4db5-a59a-875ea4d61357.png)
bbox cost는 아래와 같음 
![image](https://user-images.githubusercontent.com/46675408/179640161-ed58d3f6-6517-41c8-b47e-c008b98b7f0d.png)
  - [Generalize IoU](https://arxiv.org/pdf/1902.09630.pdf)
![image](https://user-images.githubusercontent.com/46675408/179643182-89aa6c38-cf9c-49ef-9dda-e8b4b2aa44d7.png)

triplet prediction cost는 여기에 predicate에 대한 class cost까지 합쳐서 구해짐.
이후 이 cost들로 hungarian method로 bipartite matching을 한 뒤, loss가 구해짐.
몇 번 학습하면 아래와 같이 의미없는 triplet을 내뿜는데 이를 방지하기 위해서 추가적인 IoU based 룰을 추가함.
![image](https://user-images.githubusercontent.com/46675408/179640424-d40249be-9b8d-4814-be0d-5f409188d611.png)

sub / obj class가 background고 IoU btw. gt and pred가 threshold 이상일 때, subject나 object에 대한 loss를 부가하지 않도록 함.  
![image](https://user-images.githubusercontent.com/46675408/179641129-2df53a44-6b1d-445b-85ff-ef77faf2c592.png)

- proposal C에서 파란 박스는 bbox를 잘 뽑았으니 loss를 부과하지 않는게 더 좋음
- proposal D에서 파란 박스와 주황 박스는 bbox를 잘 뽑았으니 loss를 부과하지 않는게 더 좋음

최종적인 loss는 아마 DETR에서 나왔을 entity에 대한 loss와 triplet loss를 합쳐서 계산.

### Dataset
- Visual Genome
  - 108k images, 150 entities, 50 predicates
  - Predicate classification(PredCLS) : given GT bbox and cls, predict predicates
  - Scene graph classification(SGCLS) : given GT bbox, predict predicates and object class
  - Scene graph detection : predict all!
  - Recall@k, mean RecallR@k 
- Open Image V6
  - 126k images, 288 entities, 30 predicates
  - Recall@50, weight mean average precision, phrase detection ?? 뭐라는지 잘 모르겠음.

### Implementation Details
- 2080 Ti 8대, bs=2, AdamW, weight decay 10-4, gradient clipping, Transformer LR 10-4, RestNet LR 10-5, lr dropping 0.1 by 100 epochs
- auxiliary loss 사용
DETR에서 적용한 loss 라는데 [원본](https://arxiv.org/pdf/1808.04444.pdf)읽어봐야 할듯.
-> layer 높게 쌓는데 각 layer들에 share하는 predictor 만들어서 각각 예측하고 loss 합치게 하는 것. 
![image](https://user-images.githubusercontent.com/46675408/179665520-48b53343-69dc-48cd-a52a-c9832a2f1165.png)

- 6 layers encoder, 6 triplet decoder layer, 8 head attentions
- num of entities 100, num of queries 200
- IoU threshold 0.7
- inference 2080 ti / eval 할 때 시간은 학습 시간에 안둠. 

### Results 
![image](https://user-images.githubusercontent.com/46675408/179643327-d24826ee-50d2-4d24-89e6-95f476ce9eba.png)


## 잡 생각/질문
- relation은 사실 적던 크던 많은데 annotation되거나 우리가 target 하고 있는 relation만 뽑아야 함. 
- 누가 S가 되고 누가 O가 되는지도 좀 임의적인 듯. 코 위의 눈. 눈 아래 코. -> 어쩔 수 없지..
- self-attention graph learn 관련한 연구들 좀 찾아봐야겠당
- SGG에서 relation이 없는 object들은 안뽑아도 되는건가? => relation이 있는 object들만 정답지에 있는건가? 
- Visual Genome 이랑 데이터좀 몇개 실제로 봐야겠당
- 현재 metric은 어떤 기준으로 되어 있나? ->  Scene graph detection
