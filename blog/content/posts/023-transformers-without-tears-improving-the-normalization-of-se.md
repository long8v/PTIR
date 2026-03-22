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
The vanilla Trasnformer's LayerNorm is applied after the self-attentioned output and input have been added together (residual connections). This is called the PostNorm.
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

Subsequent studies have shown that applying LayerNorm before self-attention leads to more stable learning, and is particularly effective when the layer is deep. (?) Note that one must append an additional normalization after both encoder and decoder so their outputs are appropriately scaled. -> encoder, decoder As you say one must append an additional normalization to the output of the finished (probably last layer).

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

We will use the xaiver initializer, and when we use postnorm, convergence fails because the initialization value of Xavier normal is too large. In the Transformer implementation, it is divided by sqrt(hid_dim) (**scaled** dot product), which is about sqrt(d)=22.6 for d=512. FFNs already have a small standard deviation (hid_dim, fcn_dim, where fcn_dim is roughly 4 times hid_dim, so the std for ffn is sqrt(2/(d+4d))). Suggest reducing the initializer of the attention layer as well (Small_Int)
![image](https://user-images.githubusercontent.com/46675408/164365735-77b51d6e-4ab7-4a17-8951-5b556e7a5b8f.png)

## Scaled L2 norm and FixNorm
Both batch norm and layer norm are designed to reduce covariate-shift, but [studies](https://proceedings.neurips.cc/paper/2018/hash/905056c1ac1dad141560467e0a99e1cf-Abstract.html) have shown that the real benefit comes from smoothing the loss landscape. For example, dividing by L_p norm rather than by variance gave similar or better performance in image classification.
We propose to replace LayerNorm with scaled L2 norm.
<img width="406" alt="image" src="https://user-images.githubusercontent.com/46675408/164373582-0491ea36-4c61-4eff-bcd4-48be6da53648.png">

In the last layer, the larger internality causes the output distribution to be sharper (smaller variance), which causes the frequent words to have larger numbers than the infrequent words. To improve this, it has been suggested to apply a [FixNorm](https://aclanthology.org/N18-1031.pdf) to the last layer.
<img width="74" alt="image" src="https://user-images.githubusercontent.com/46675408/164373831-ecf33f25-b3c3-496d-8a01-0bcfb9094d79.png">

To make the parameter g trainable, ScaleNorm and FixNorm can be applied at once, and can be written as follows.
<img width="394" alt="image" src="https://user-images.githubusercontent.com/46675408/164374200-bdc55467-28df-44cf-be17-4a379cf6a5eb.png">

In this expression, the last layer is equal to cosine normalization (Luo et al., 2018) with a learned scale.

<img width="930" alt="image" src="https://user-images.githubusercontent.com/46675408/164374623-6d942207-3b55-4e8e-aba6-1ad859799535.png">

<img width="453" alt="image" src="https://user-images.githubusercontent.com/46675408/164374657-e37d7104-3227-466e-a055-caa8cddd69bb.png">

PreNorm converges faster and performs better after convergence
FixNorm converges faster, but the converged performance is similar to that of
Better performance when applying FixNorm + ScaleNorm
ScaleNorm is slower to converge with warmup, and the performance is similar to that without warmpup.

<img width="452" alt="image" src="https://user-images.githubusercontent.com/46675408/164374680-c95262a0-8894-4075-af5c-6fd9568dd797.png">
