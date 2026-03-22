---
title: "[43] Relation Transformer Network"
date: 2022-08-01
tags: ['2020Q2', 'SGG', 'graph']
paper: "https://arxiv.org/pdf/2004.06193.pdf"
issue: 49
issueUrl: "https://github.com/long8v/PTIR/issues/49"
---
<img width="682" alt="image" src="https://user-images.githubusercontent.com/46675408/182097267-efbad1f2-3431-49f1-9d4e-f9249f9372cb.png">

[paper](https://arxiv.org/pdf/2004.06193.pdf)

## TL;DR
- **task :** bbox가 주어졌을 때의 Scene Graph Generation
- **problem :** object pair 간의 관계를 모델링을 더 잘하고 싶다. 
- **idea :** object 간의 context를 학습하는 것이 도움이 되고, 또 predicate를 예측할 때에도 그 해당된 object 뿐 아니라 다른 모든 object가 참고되면 더 좋다
- **architecture :** transformer encoder-decoder를 잘 따와서, node간 관계는 self-attention으로, edge의 관계는 cross-attention으로 모델링 하자. 
- bbox가 주어졌을 때, 1) Faster RCNN으로 visual feature 뽑고, 2) transformer encoder에 넣어서 self-attention output도 뽑고 bbox내 클래스도 예측한다 3) transformer decoder에 Edge Query를 넣고 1, 2에서 나온 feature들과 cross-attention을 한 뒤에 4) FCN 태워서 subject, object, relation 예측한다.
- **objective :** subject, object, relation의 cross entropy loss
- **baseline :** IMP, ... 등 two-stage models.
- **data :**  Visual Genome, CQA, VRD
- **result :** SOTA
- **contribution :** Transformer 구조를 열심히 이용. 
 
## Details
### why two-stage?
이전에 읽었던 one-stage와 달리 bbox가 input으로 들어감!
즉 최종 output에 bbox가 있냐 없냐의 차이.

### Architecture
<img width="666" alt="image" src="https://user-images.githubusercontent.com/46675408/182113783-89769ac1-46b1-4302-acdb-4e2ba0ada45b.png">

#### Problem Decomposition
- image I에서 우리가 원하는 scene graph G로 만드는 과정을 조건부 확률로 표현할 수가 있음. (R은 relation, O는 object class, B는 bbox, I는 이미지)
$P(R|O,B,I)P(O|B,I)P(B|I)$
  - 여기서 $P(B|I)$를뽑는건 object detection이 함
  - $P(O|B,I)$를 뽑을 때는, object간 context를 학습 할 수 있는 N2N 모듈을 사용함.
  - $P(R|O,B,I)$ 부분은 E2N 모듈을 통해 entity들과 query에 대해 undirected edges를 만들고 candidate들을 뽑은 뒤, RPM이 edge direction과 relation type을 구함.
- 두 object 간에 unique relation type를 가정했다. 

#### Object Detection
VGG16 backbone의 Faster RCNN을 쓸거다. 
node $n_i$가 주어졌을 때 spatial embdding인 bbox coordinate을 뽑고, VGG16의 가장 위 레이어에서 feature map $I_{feature}$를 뽑아 4096 차원의 feature vector $v_i$들을 뽑는다.  
$o_i^{init}\in\mathbb{R}^C$의 경우 (C는 # of classes), GloVE 임베딩을 사용해서 초기화해줬다.  

#### Encoder N2N Attention 
object들의 context를 학습하는 것은 object detection 분 아니라 relation 분류를 할 때도 도움이 된다. 
이러한 목적으로 object 들을 트랜스포머 인코더에 넣는다. 이때 들어가는 input은 아래와 같다. $v_i$는 image feature vector $s_i$는 object detection에서 나온 class label에 대한 GloVe 벡터 $b_i$는 bounding box다.
<img width="153" alt="image" src="https://user-images.githubusercontent.com/46675408/182112453-be6998be-cd4b-433a-a8cf-a4b470c85354.png">

그리고 아래의 네트워크를 태운다. 그리고 마지막 레이어에서 해당 bbox에 대한 분류를 하게 된다. 
<img width="224" alt="image" src="https://user-images.githubusercontent.com/46675408/182112464-71825dc6-8047-47f1-921b-15be1d08caaf.png">

또 $f_i^{final}$은 decoder cross-attention으로 들어가게 된다.

#### Decoder Edge Positional Encoding
transformer decoder에 Edge query를 넣어주고 싶은데, 사실 edge에 대해서는 순서가 없기 때문에 PE를 넣기가 애매하다. 
<img width="333" alt="image" src="https://user-images.githubusercontent.com/46675408/182115288-7278589e-f580-440d-9401-39730597e050.png">

그래서 위와 같이하면 뭐가 subject고 object인지 알 수 있게 된다. (?? 사실 식이 이해가 잘 안됨) 

#### Decoder E2N Attention
Edge Queries내 $e_{ij}$랑 위의 부수적인 벡터 
<img width="172" alt="image" src="https://user-images.githubusercontent.com/46675408/182116604-3d13b040-70f6-4d3f-ba87-07f9f94aac13.png">

<img width="243" alt="image" src="https://user-images.githubusercontent.com/46675408/182116572-6b922922-faa1-4cf4-9640-6b3a525807d1.png">

edge간 self-attention 하는건 성능 향상에 도움이 안돼서 바로 cross-attention하는 방식으로 진행이 되었다.

#### Directed Relation Prediction Module(RPM)
relation은 방향이 있어서, 위에서 rich한 임베딩들을 가져와서 아래와 같이 directional relational embedding을 만들어주었다.
<img width="545" alt="image" src="https://user-images.githubusercontent.com/46675408/182117015-64375cad-f035-4048-8be5-7dc4f087e1fe.png">

그리고 RPM(relation prediction module)이라고 하는 모듈에 위의 임베딩을 넣어줘서 최종 relation을 예측한다.

<img width="264" alt="image" src="https://user-images.githubusercontent.com/46675408/182117900-9f010692-7863-41fb-be13-7eb5dc5e6f3a.png">

LayerNorm -> Linear -> ReLU -> Linear(최종 relation categories) -> softmax 취해주기

frequency에 대한 값도 넣어줬다. 
<img width="468" alt="image" src="https://user-images.githubusercontent.com/46675408/182118011-fc72d855-857f-483b-b6ba-c9ae4600e4e2.png">

### Implementation Details
object detector에서 NMS(IoU > 0.3)를 통해 나온 top 64개의 object label을 사용했고, relation classification의 **계산비용을 줄이기 위해 노드 페어 중 바운딩 박스가 겹치는 부분만 고려했다!**(엄청 큰 inductive bias..)

### Result
#### Visual Genome
![image](https://user-images.githubusercontent.com/46675408/182268663-01f0840e-40af-49d6-b1be-d5274f8e0cd1.png)

#### Qualitative 
 
![image](https://user-images.githubusercontent.com/46675408/182268694-1e1f6ea3-0557-476d-b7fc-2a19eb1b46d3.png)

(b)는 N2N attention heatmap. 한 object가 다른 object에 얼마나 영향을 줬냐.
(c)는 E2N attention heatmap. object 들이 relation에 얼마나 영향을 줬냐.

on을 of로 틀리는 경우가 많았는데 보면 `Face, of, Woman`처럼 of가 더 자연스러운 경우가 많았다. -> multi-predict가 필요한 이유인듯

![image](https://user-images.githubusercontent.com/46675408/182270554-369e8f4d-f6c6-411f-80c3-09a13e050f49.png)

decoder 그냥 transformer꺼 쓰는 것(self-attention 들어간거)보다 우리꺼 쓰는게 나았다.

![image](https://user-images.githubusercontent.com/46675408/182270212-8d2990f8-2605-47d1-b228-bf3b4a762690.png)

decoder에서 각 feature를 뺐을 때의 성능 drop은 아래와 같았다. frequency가 좀 쎈듯.

각각에 대한 저자들의 설명 
![image](https://user-images.githubusercontent.com/46675408/182270446-a32a687c-35c9-4347-8046-0e817e3b9dfa.png)
