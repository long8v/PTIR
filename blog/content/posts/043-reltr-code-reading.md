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

- Understand how bipartite matching works
- The final output will look like (batch_size, num_of_triplets, -1).
- If we define a cost function (=classification error with gt + bbox error) in each dimension (bbox, since the classification output will be separate) and summarize it, it will look like (batch_size, num_of_triplets, cost) and use the scipy package to get an index that minimizes cost and matches all gt!
- What happens to inference then??? -> this is DETR again