---
title: "[106] Prefix-Tuning: Optimizing Continuous Prompts for Generation"
date: 2023-03-28
tags: ['2021Q1', '25min', 'finetuning', 'LLM', 'ACL']
paper: "https://aclanthology.org/2021.acl-long.353.pdf"
issue: 115
issueUrl: "https://github.com/long8v/PTIR/issues/115"
---
<img width="778" alt="image" src="https://user-images.githubusercontent.com/46675408/228103645-5a064341-7b31-4142-9051-fbca465348a5.png">

[paper](https://aclanthology.org/2021.acl-long.353.pdf)

## TL;DR
- **I read this because.. :** efficient finetuning 시리즈 물
- **task :** LLM finetuning
- **problem :** finetuning 다 하는거 비효율적. discrete prompt 찾기 계산 비효율적.
- **idea :** continuous한 prompt를 앞에 붙이자. 
- **architecture :** BART, GPT-2
- **objective :** ce loss
- **baseline :** finetuning, finetuning top 2 layer, apdapter
- **data :** E2E, WebNLG, DART 
- **result :** finetuning 보다는 살짝 낮고 adapter나 ft-top2보단 조금 나은 성능 
- **contribution :** #113 랑 비슷한 아이디어 

## Details
<img width="445" alt="image" src="https://user-images.githubusercontent.com/46675408/228104356-216263dd-6ecd-49c6-9e53-54441e9e602c.png">

PLM이 따로 있고 prefix를 위한 hidden 차원의 matrix $P_\theta $가 있는 형태
<img width="381" alt="image" src="https://user-images.githubusercontent.com/46675408/228108123-3755df18-6d09-4a19-a258-79fbffd9617f.png">

<img width="858" alt="image" src="https://user-images.githubusercontent.com/46675408/228104383-4744b8ac-5965-42f2-8435-3fdd4baf441b.png">

smaller matrix $P_\theta '$에서 시작해서 MLP로 size 키우는게 더 성능이 좋았다. 학습하고 나서는 $P_\theta '$없이 바로 prefix $P_\theta $를 사용하면 된다 

### Results
<img width="821" alt="image" src="https://user-images.githubusercontent.com/46675408/228108486-a27ffbce-c333-4a43-8d82-4f51235e265e.png">


### Ablations
- low data 상황일 때 random initalize보다 real word로 init하는게 좋았다.
<img width="423" alt="image" src="https://user-images.githubusercontent.com/46675408/228107390-869dd879-7fa7-42aa-bb31-b0a129d8d176.png">

태스크와 관련 없는 "elephant" 같은 것도 random 보다 나았다. full일때는 Initialize에 크게 영향 받지 않았다.

- prompt 길이는 task 마다 성능의 상향선이 있었다
요약은 200 / table to text는 10 
<img width="424" alt="image" src="https://user-images.githubusercontent.com/46675408/228107654-790dec8c-7f18-4c4a-ad5b-c8b88aa706a1.png">

- prompt를 앞에 두는 prefix 형태가 $[x; prompt; y]$ 형태인 infix보다 성능이 좋았다.
<img width="392" alt="image" src="https://user-images.githubusercontent.com/46675408/228108578-cf3d8c3b-188f-4df5-ae56-4d795997220c.png">
