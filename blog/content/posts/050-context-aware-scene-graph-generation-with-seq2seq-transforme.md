---
title: "[44] Context-Aware Scene Graph Generation With Seq2Seq Transformers"
date: 2022-08-02
tags: ['ICCV', '2021Q4', 'SGG', 'graph']
paper: "https://openaccess.thecvf.com/content/ICCV2021/papers/Lu_Context-Aware_Scene_Graph_Generation_With_Seq2Seq_Transformers_ICCV_2021_paper.pdf"
issue: 50
issueUrl: "https://github.com/long8v/PTIR/issues/50"
---
![image](https://user-images.githubusercontent.com/46675408/182299681-48ec68cd-16ff-48cb-be0e-1d605f20b272.png)

[paper](https://openaccess.thecvf.com/content/ICCV2021/papers/Lu_Context-Aware_Scene_Graph_Generation_With_Seq2Seq_Transformers_ICCV_2021_paper.pdf)

## TL;DR
- **task :** two-stage Scene Graph Generator
- Problem :** Existing studies assume that triplets are independent and make parallel predictions.
![image](https://user-images.githubusercontent.com/46675408/182321537-9620b7b3-dd75-44b2-901d-767246932482.png)
- **idea :** If you look at other predicted relations and make auto-regressive predictions, you'll do better! (see above)
- **architecture :** It is a transformer encoder-decoder structure, where the decoder puts the value from the encoder into [S, P, O] with the embedding for the relation, which is self-attentive, and the value from the encoder is cross-attentive.
- **objective :** add a reinforcement learning approach to cross entropy loss + recall, mRecall
- **baseline :** Graph R-CNN, ... 
- **data :** VRD, Visual Genome
- **result :** SOTA
- **contribution :** An auto-regressive approach first seen at SGG
- **limitation or part I don't understand :** It's interesting to learn... -> (after discussion) multi-object detection also had a case of putting them sequentially. (Learning that if there is a cat in this picture, there will be a dog.) Transformer decoders don't just look at the input information, but also cross-attention, so the input doesn't necessarily have to be related to what I want to select.

## Details
### Architecture
![image](https://user-images.githubusercontent.com/46675408/182309482-7226450d-aba3-409d-92fb-52cba8d4fa64.png)

#### Object Encoder
Just a transformer encoder. But I'm not sure what you put as input. Is it just a visual feature map?
X_b$ is the output of the bth transformer block

#### Relationship Decoder 
Takes the contextualized object features $X_B\in \mathbb{R}^{N\times D}$ (where N is the number of objects and D is the embedding dimension) and the predicted relationship $\hat Y_{1:m}$ up to the previous step, and picks the m(+1) relationship.

The input to the decoder is the concatenation of the contextualized embedding of the subject, the contextualized embedding of the object, and the previously extracted embeddings for the relation. $(X_B[i], E[r], X_B[j])$
So it's an unusual structure where you embed the previous prediction and get the next one. Concatenate the D-dimensional ffn and pass it through self-attention and cross-attention. Initially, we just put in a D-dimensional `<SOS>`.
For cross-attention, it comes from hanging $Y_k$ from the decoder's self-attention and $X_B$ from the encoder.
![image](https://user-images.githubusercontent.com/46675408/182317261-bf6a0992-c921-47fd-b76d-e3fc03cd4053.png)

Predict the next relationship triplet with the output $Y_K$ from the last Kth decoder layer.
Predicted for all remaining pairs as shown below. And the one with the highest softmax is selected.
![image](https://user-images.githubusercontent.com/46675408/182317929-c9517580-c105-454a-b3d8-bfec471a78ed.png)

$i$ : subject indices, $j$ : object indicies

### Training scheme
- Triplet ordering is learned by shuffling.
- The loss is originally only added for positive pairs, but VRD also adds negative pairs because it is important to predict no relation.
![image](https://user-images.githubusercontent.com/46675408/182318147-23727fe6-686a-484c-bc9d-69e982b4921e.png)

### Reinforcement Learning
1) In training, we get input history as GT (teacher-forcing), but not in inference 2) There is a gap between cross entropy loss and recall. -> Add a reinforcement learning component when decoding.
Recall and mRecall tend to move in opposite directions. So we add alpha and define it as reward.
![image](https://user-images.githubusercontent.com/46675408/182319646-38879f45-4594-48ed-a536-c5629538faf2.png)

![image](https://user-images.githubusercontent.com/46675408/182319766-5d2f29dd-3c4b-498d-b66d-3b6304f71811.png)

Here, action is what to choose when the logit value is given for all pairs. state is the state of selecting m pairs. RL is better than greedy decoding.

### Expreiments
![image](https://user-images.githubusercontent.com/46675408/182318546-1b1748ec-cb5b-4d37-822a-9b83a481bcaa.png)


#### Qualitative Results
![image](https://user-images.githubusercontent.com/46675408/182320660-297c2a54-485e-4aa5-b66b-e72d4e908b7b.png)

The probability of guessing GT is higher than predicting it independently.
