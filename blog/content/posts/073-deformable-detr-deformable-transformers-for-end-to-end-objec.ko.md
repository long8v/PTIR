---
title: "[67] Deformable DETR: Deformable Transformers for End-to-End Object Detection"
date: 2022-09-21
tags: ['2020Q3', 'ICLR', 'long', 'object detection', 'SenseTime']
paper: "https://arxiv.org/abs/2010.04159"
issue: 73
issueUrl: "https://github.com/long8v/PTIR/issues/73"
---
<img width="625" alt="image" src="https://user-images.githubusercontent.com/46675408/191400328-e6a48a25-6e6f-42cc-8f95-b05be108787b.png">

[paper](https://arxiv.org/abs/2010.04159), [code](https://github.com/fundamentalvision/Deformable-DETR)

## TL;DR
- **task :** object detection, efficient transformer
- **problem :** DETR 작은 object에 대해 성능이 낮고, $O(n^2)$ 연산이 비효율적이다
- **idea :** deformable convolution에서 착안해서 주어진 input feature map의 point에서 얼마나 떨어진 픽셀들(=sampling offset)과 attention을 할지를 정하는 deformable attention module을 정의한다. 
- **architecture :** DETR에서 encoder 부분을 deformable attention module로 바꾸고, decoder 부분에서는 SA는 그대로 두고 CA를 deformable로 바꿈. 이걸 또 multi-scale로 함. 추가적으로 2-staged deformable DETR을 제안하는데 deformable DETR encoder 사용하여 region proposal 먼저 하고 decoder를 위에 쌓아서 cls 예측함.  
- **objective :** DETR loss를 따라가되 bbox cls에 대해 focal loss 적용(DETR은 그냥 NLL loss 사용)
- **baseline :** DETR, Faster-RCNN
- **data :** COCO 2017
- **result :** 성능 SOTA. DETR 대비 10배 빠른 수렴 속도. Faster RCNN + FPN과 DETR-DC5와 비슷한 FLOPS이나 runtime은 1.6배 빠름. 
- **contribution :** efficient DETR + DETR with FPN

## Details
<img width="502" alt="image" src="https://user-images.githubusercontent.com/46675408/191400394-6c76b7c4-82e3-4fd9-bd5c-6df2455d8569.png">

### Deformable Attention Module 
<img width="552" alt="image" src="https://user-images.githubusercontent.com/46675408/191400443-75b8a21b-8d52-48c9-bd36-13ddaf3604c9.png">

<img width="559" alt="image" src="https://user-images.githubusercontent.com/46675408/191400507-0eae8a8a-3956-4015-8f24-a3f8d96dced0.png">

### Multi-scale Deformable Attention Module
<img width="738" alt="image" src="https://user-images.githubusercontent.com/46675408/191416123-bf72d457-2b50-4eb5-8413-64e305bd7bbb.png">

- L이 feature scale 
- normalize 해줘서 multi-scale 그냥 한번에 처리 가능하기 때문에 합해서 사용 -> feature pyramid network처럼 서로 정보 교환을 위한 별도의 디자인 필요 없음! 

#### Deformable Transformer Encoder
- reference point는 모든 query pixel.
- w, h로 정규화해주기 때문에 어느 scale의 feature에서 온건지 정보를 주려고 2D PE에다 scale-level embedding을 추가함
- 저기서 sampling offset인 $\Delta p_{mqk}$와 attention weight $A_{mqk}$는 query feature $z_q$를 linear 태워서 만들어준다.
- ResNet의 stage C3~C5 feature map 쓰고 1x1 conv로 channel size 256로 맞춰줌
- C6은 C5에 3 x 3 conv stride 2 준거!
![image](https://user-images.githubusercontent.com/46675408/202976101-554abb00-7878-4fc1-8b36-271099d12bd1.png)
- 그림이 한 픽셀에 대해서만 그려져 있어서 헷갈리는데 결국 저걸 모든 픽셀에 대해서 하니까 attention까지 하고 난게 원래의 feature map 크기로 생길거고 그게 레이어 쌓여가면서 계속 업데이트 되는 형태!


#### Deformable Transformer Decoder
- deformable attention 자체가 convolutional feature를 활용하려고 만든거기 때문에 SA는 그대로 두고 CA만 
- reference point는 object query에 linear + sigmoid로 예측하도록 하고 이후에 Deformable Attention 연산
- 이 때 feature map은 encoder의 output feature maps from the encoder을 씀.
- bbox는 reference point의 상대적인 offset으로 예측하도록 함. reference point는 box center의 초기값으로 사용됨. 즉 bbox regression을 하면 reference point로 부터 dx, dy, w, h를 예측하는 문제를 풀면 됨!  
![image](https://user-images.githubusercontent.com/46675408/191904394-28a2e484-f580-4990-be0f-84a72e66a184.png)
- 레이어가 쌓여가면서 계속 업데이트 받는건 query feature인듯 함! object query만큼의 query feature가 레이어가 쌓이면서 계속 올라가는 형태

### Additional Improvements and Variants for deformable DETR
#### Iterative Bounding Box Refinement
(d - 1)번째 레이어의 bbox 예측값을 가지고 d번째 레이어의 bbox 예측을 refine하는 과정이 필요
![image](https://user-images.githubusercontent.com/46675408/191907763-5c3deec3-734c-4b5f-aa27-b18a71f080ff.png)

initial 값은 x, y는 reference point, qw, wh = 0.1로 설정했다.
(d - 1)번째 레이어의 bbox 중앙 좌표가 d번째 레이어의 reference point가 되는 형태임. box size도 역시 $\Delta$를 사용해서 같이 가도록 함
$sigma^{(-1)}$부분은 gradient 안흐르게 함.

#### Two-Stage Deformable DETR
원래의 detr은 object query가 이미지랑 전혀 상관없는 걸 봄. region proposal을 먼저 하고 이를 object query로 던져주는 방식!
region proposal은 deformable DETR의 encoder만 사용하고 모든 픽셀에 대한 feature가 object query가 되어 bbox를 예측한다. => Hungarian Loss로 학습 됨.
top scored 된 bbox들은 뽑혀서 DETR decoder의 iterative bounding box refinement의 초기값으로 사용되고 그 coordinate들의 PE가 object query로 던져진다. 

![image](https://user-images.githubusercontent.com/46675408/191908950-09fb073c-5fa9-446e-b9a6-71aafc2b0db4.png)

### Result
<img width="766" alt="image" src="https://user-images.githubusercontent.com/46675408/191415998-b96160f7-cf16-4257-8d92-6569e3f84ac4.png">

<img width="754" alt="image" src="https://user-images.githubusercontent.com/46675408/191416067-40e82c43-8346-47a0-893f-9406ebf2834b.png">

### Training details
- 50 epochs
- backbone : ImageNet pretrained ResNet-50
- M(=# of attention head) : 8, K(=# of sampled key in each feature level for each attention head) : 6
- lr = 2e-4, learning decay 0.1 40th epoch
- bbox classification loss weight 2 
- linear projection for query reference points and sampling offsets 0,1
<img width="553" alt="image" src="https://user-images.githubusercontent.com/46675408/199367568-3c1e1ba1-122b-4f3d-b7f8-0a8720dc40f3.png">
