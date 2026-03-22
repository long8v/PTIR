---
title: "Interpretable Image Classification with Differentiable Prototype Assignment"
date: 2022-11-09
tags: ['2022Q3', 'ECCV', 'XAI']
paper: "https://arxiv.org/abs/2112.02902"
issue: 85
issueUrl: "https://github.com/long8v/PTIR/issues/85"
summary: "reduce prototypes"
---
<img width="988" alt="image" src="https://user-images.githubusercontent.com/46675408/200740122-30475a8a-4f84-492d-a8c9-4fd306d15091.png">

[paper](https://arxiv.org/abs/2112.02902)

## TL;DR
- **task :** case-based reasoning 
- **problem :** The existing ProtoPNet assumes a prototype for each class, and since the optimization is divided into multiple steps and looks at the absence of a prototype when deciding on a class, the prototype becomes vague.
- **idea :** 1) allow prototypes to be shared between classes 2) make it differentiable to assign a prototype to a class 3) define a focal similarity function so that backgrounds, etc. are not made from prototypes
- **architecture :** Looks exactly like ProtoPNet. CNN => get focal similarity with prototype => soft assign with gumbel softmax => pooling => classifier
- **objective :** CE loss(h learning) + orthogonality loss
- **baseline :** ProtoPNet 
- **data :** CUB-200-2011, Standford Cars Data  
- **result :** SOTA, capture more salient features 
- **contribution :** reduce prototypes 
- **limitation or part I don't understand :** fig 3 doesn't make sense to me exactly... prototype pool is shared but there are separate slots for each class and those prototypes are categorized?

## Details
### Preliminaries: ProtoPNet(prototypical part network)
[This Looks Like That: Deep Learning for Interpretable Image Recognition](https://arxiv.org/pdf/1806.10574.pdf)
I want to visualize why this image was categorized into this class.
<img width="728" alt="image" src="https://user-images.githubusercontent.com/46675408/200739394-422cac33-6576-42f8-b2ae-4c8675c73e07.png">

Given an image x, draw f(x) with a CNN and get H x W x D as CNN output
At the same time, m prototypes have $H_1$ x $W_1$ x D shape, which must be smaller than H and W.
In this case, the D dimensions are the same, but the height and width are smaller, so each prototype can be used like a CNN patch to get an activation map

<img width="625" alt="image" src="https://user-images.githubusercontent.com/46675408/200739415-e5119553-d331-43e4-bf9d-08322ba2bd4e.png">

The overall ProtoPNet structure is the same as above.
Learning is divided into three phases
(1) Stochastice gradient descent(SGD) of layers before last layer
learns a prototype P and a convolution filter. loss learns the minimum distance between the last classification loss and the patches in the prototype and convolution output to be closer if they are of the same class and farther if they are of different classes.
<img width="719" alt="image" src="https://user-images.githubusercontent.com/46675408/200739532-7b8bcc35-7863-4af4-aecc-2b27d99a7c22.png">

(2) Projection of prototypes
Assigns prototype to be the closest patch in the same class as the prototype
<img width="593" alt="image" src="https://user-images.githubusercontent.com/46675408/200739733-c74e70ff-2b28-43e1-9bc6-f4439fceee26.png">

(3) Convex optimization of last layer
Freeze the prototype and CNN and learn the matrix for h.
<img width="509" alt="image" src="https://user-images.githubusercontent.com/46675408/200739835-3338cbbf-aa87-4c24-b998-af62c3f8adb0.png">

- The logic behind the model's classification
<img width="1409" alt="image" src="https://user-images.githubusercontent.com/46675408/200740394-1db4df0d-993d-4208-b911-9707ae54e88c.png">

- How it differs from CAM or partial attention
<img width="1240" alt="image" src="https://user-images.githubusercontent.com/46675408/200740420-2ae3cabb-d846-477b-8b6d-babc39844c1f.png">

### motivation 
<img width="1030" alt="image" src="https://user-images.githubusercontent.com/46675408/200740577-979ed099-14df-42e3-8b8e-3cf94729d3f1.png">

### Architecture
<img width="1026" alt="image" src="https://user-images.githubusercontent.com/46675408/200740957-d76b21d0-d130-4427-bb9c-ae06739c80a9.png">

Each class has K slots, so you can assign shared prototypes to them

Given an image x, draw the output H x W x D with CNN(=f(x))
This can be interpreted as having H x W vectors in D dimensions. We can assign those D-dimensional vectors to the kth slot by finding their similarity

#### Focal similarity 
Previous studies, such as ProtoPNet, have obtained similarity as follows
<img width="308" alt="image" src="https://user-images.githubusercontent.com/46675408/200741464-c7890e76-2704-4609-8d91-3f1fee9dfb71.png">

<img width="253" alt="image" src="https://user-images.githubusercontent.com/46675408/200741575-5927fd74-2677-43cd-8a05-f0cc9f07abfe.png">

However, this can lead to (1) all the patches of f(x), z, being prototypically similar, i.e., focusing only on the background, and (2) gradienting only the activated elements in the image. To avoid this, we propose focal similarity
<img width="483" alt="image" src="https://user-images.githubusercontent.com/46675408/200741686-95d91487-6bcf-48e6-92e9-8ee9619dad6b.png">

<img width="1008" alt="image" src="https://user-images.githubusercontent.com/46675408/200742058-0a90fc04-f110-4287-8cbe-95ae40722386.png">

#### Assigning one prototype per slot
gumbel-softmax to soften the prototype instead of hard assigning it and allow the gradient to flow

<img width="583" alt="image" src="https://user-images.githubusercontent.com/46675408/200743507-eb892c51-d77f-4694-8ba8-0a13273557e4.png">

Add more LOS to prevent multiple prototypes from fitting in one slot.
<img width="393" alt="image" src="https://user-images.githubusercontent.com/46675408/200742122-810671f0-bc43-43a1-9d95-8b8e27685e11.png">
