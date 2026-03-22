---
title: "RelTR code reading"
date: 2022-07-21
tags: ['2022Q1', 'SGG']
paper: ""
issue: 43
issueUrl: "https://github.com/long8v/PTIR/issues/43"
---
## RelTR code reading
https://github.com/yrcong/RelTR
https://github.com/long8v/PTIR/issues/40

- bipartite matching이 어떻게 되는지 알겠음
  - 최종적인 output은 (batch_size, num_of_triplets, -1) 처럼 됨.  
  - cost function(=gt와의 classification 에러 + bbox 에러)를 각각의 차원(bbox, classification output은 따로 나올 것이므로)에서 정의하여 summation하면 (batch_size, num_of_triplets, cost)처럼 될 것이고 이를 scipy 패키지 사용하면 cost를 최소화하며 모든 gt와 매칭되는 index가 나옴!
  - inference는 그럼 어떻게 되는거지??? -> 이건 DETR 다시 읽자