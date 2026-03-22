---
title: "[22] Transformers without Tears: Improving the Normalization of Self-Attention"
date: 2022-04-21
tags: ['NLP', '2019', 'fundamental', 'norm']
paper: ""
issue: 23
issueUrl: "https://github.com/long8v/PTIR/issues/23"
---
![image](https://user-images.githubusercontent.com/46675408/164357772-6abe3379-3d92-4e4f-a5d7-9925be36da0c.png)

## pre-norm vs post-norm
vanilla Trasnformer의 LayerNorm은 self-attention을 거친 output과 input을 더한 뒤(residual connection)에 적용된다. 이를 PostNorm이라고 부른다.
![image](https://user-images.githubusercontent.com/46675408/164364130-fb7f3982-5665-4ffe-9150-861c94c67036.png)

```
    def forward(self, src, src_mask):
        
        #src = [batch size, src len, hid dim]
        #src_mask = [batch size, 1, 1, src len] 
                
        #self attention
        _src, _ = self.self_attention(src, src, src, src_mask)
        
        #dropout, residual connection and layer norm
        src = self.self_attn_layer_norm(src + self.dropout(_src))
```

후속 연구에서 self-attention을 거치기 전에 LayerNorm을 적용하는 것이 더 안정적인 학습을 하게 하고, 특히 레이어가 깊어질 때 효과적임이 밝혀졌다. (?) Note that one must append an additional normalization after both encoder and decoder so their outputs are appropriately scaled. -> encoder, decoder 끝난(아마 마지막 layer) output에 대해 Norm 추가로 해야한다고 하는듯. 

![image](https://user-images.githubusercontent.com/46675408/164364363-e1b20a96-d6c9-4a46-b529-d28af478f6c2.png)

```
    def forward(self, src, src_mask):
        
        #src = [batch size, src len, hid dim]
        #src_mask = [batch size, 1, 1, src len] 
                
        #self attention
        src_norm = self.self_attn_layer_norm(src)
        _src, _ = self.self_attention(src_norm, src_norm, src_norm, src_mask)
        
        #dropout, residual connection and layer norm
        src = self.self_attn_layer_norm(src + self.dropout(_src))
```

## weight initializer
![image](https://user-images.githubusercontent.com/46675408/164365920-3574e890-16fc-4f12-935c-c00273b488f1.png)

xaiver initializer를 사용하게 되는데, postnorm을 쓸 경우에 수렴에 실패하는 경우가 생긴다. 그 이유는 Xavier normal의 초기화값이 너무 크기 때문이다. Transformer 구현에서 sqrt(hid_dim)으로 나누게 되는데 (**scaled** dot product), 이는 d=512일 때 sqrt(d)=22.6정도 된다. FFN은 이미 작은 standard deviation이 작기 때문에 (hid_dim, fcn_dim인데 fcn_dim이 대충 hid_dim의 4배정도로 잡나봄, 즉, ffn의 std는 sqrt(2/(d+4d))정도 됨). attention layer의 initializer도 그렇게 줄이는 걸 제안(Small_Int)
![image](https://user-images.githubusercontent.com/46675408/164365735-77b51d6e-4ab7-4a17-8951-5b556e7a5b8f.png)

## Scaled L2 norm and FixNorm
batch norm과 layer norm 모두 covariate-shift를 줄이기 위해 고안되었으나, 실제로는 loss landscape를 부드럽게 만드는데에서 온다는 [연구](https://proceedings.neurips.cc/paper/2018/hash/905056c1ac1dad141560467e0a99e1cf-Abstract.html)가 있었다. 가령, variance로 나누는 것이 아닌 L_p norm으로 나누었을 때 이미지 분류에서 비슷하거나 더 나은 성능을 보였다.
우리는 LayerNorm을 scaled L2 norm으로 바꾸는것을 제안한다.
<img width="406" alt="image" src="https://user-images.githubusercontent.com/46675408/164373582-0491ea36-4c61-4eff-bcd4-48be6da53648.png">

마지막 레이어에서 내적이 커지면 output distribution이 sharp해지고(분산이 작아지고) 이는 자주 나온 단어가 그렇지 않은 단어보다 더 수치가 커지게 한다. 이를 개선하기 위해 [FixNorm](https://aclanthology.org/N18-1031.pdf)을 마지막 레이어에 적용하는것이 제안되었다. 
<img width="74" alt="image" src="https://user-images.githubusercontent.com/46675408/164373831-ecf33f25-b3c3-496d-8a01-0bcfb9094d79.png">

이때 파라미터 g를 학습가능하게 하기 위하여 ScaleNorm과 FixNorm을 한번에 적용할 수 있고, 아래와 같이 쓸 수있다. 
<img width="394" alt="image" src="https://user-images.githubusercontent.com/46675408/164374200-bdc55467-28df-44cf-be17-4a379cf6a5eb.png">

이 식에서 마지막 레이어는 cosine normalization (Luo et al., 2018) with a learned scale와 같다.

<img width="930" alt="image" src="https://user-images.githubusercontent.com/46675408/164374623-6d942207-3b55-4e8e-aba6-1ad859799535.png">

<img width="453" alt="image" src="https://user-images.githubusercontent.com/46675408/164374657-e37d7104-3227-466e-a055-caa8cddd69bb.png">

PreNorm이 수렴도 빠른데 수렴 이후 performance도 좋음
FixNorm을 적용하면 수렴은 빨리하는데 수렴한 성능은 유사
FixNorm + ScaleNorm을 적용하면 성능 더 좋음
ScaleNorm은 warmup 쓰면 수렴이 느리고, 성능도 warmpup 안쓴거랑 비슷하게 나옴.

<img width="452" alt="image" src="https://user-images.githubusercontent.com/46675408/164374680-c95262a0-8894-4075-af5c-6fd9568dd797.png">
