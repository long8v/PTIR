---
title: "Visual ChatGPT: Talking, Drawing and Editing with Visual Foundation Models"
date: 2023-03-30
tags: ['GPT', '2023Q1']
paper: "https://arxiv.org/pdf/2303.04671.pdf"
issue: 116
issueUrl: "https://github.com/long8v/PTIR/issues/116"
summary: "GPT Series. Talked about in many places. - The first? vision chatGPT"
---
<img width="1009" alt="image" src="https://user-images.githubusercontent.com/46675408/228726791-d0115425-a8ee-49d5-962b-3997c632bb14.png">

[paper](https://arxiv.org/pdf/2303.04671.pdf), [github](https://github.com/microsoft/visual-chatgpt), [demo](https://huggingface.co/spaces/microsoft/visual_chatgpt) 

## TL;DR
- **I read this because.. :** GPT series. It's been talked about in various places.
- **task :** chatGPT with visual input output
- **problem :** chatGPT only communicates with language. It would be nice to receive image input/output, but if chatGPT also receives a vision model, it will take too long to learn the model.
- **idea :** Let's just make a system that can call external Vision Foundation Models -> chain of thought to think about which vision model to call - do action. -> Make a system that can rephrase ambiguous queries to fit the chat interface and quote the image files you create.
- **architecture :** vision models collected from hf etc + chatGPT based on instructGPT + apply system through [LangChain](https://github.com/hwchase17/langchain)
- **objective :** LM ce loss 
- **baseline :** x 
- **data :** does not appear to be newly learned
- **evaluation :** qualatatively 
- **result :** Working
- **contribution :** The first? vision chatGPT
- **limitation / things I cannot understand :** I thought it was a flamingo-like model, but it wasn't.. something feels more like an instruction manual than a model .. not fancy, but in the future, this approach will be the mainstream...

## Details

<img width="505" alt="image" src="https://user-images.githubusercontent.com/46675408/228727201-c43301c5-fd8a-47fb-a43e-d3b6177e1734.png">

visual foundation models + MaskFormer in hf
`Since Visual ChatGPT is a text language model, Visual ChatGPT must use tools to observe images rather than imagination. The thoughts and observations are only visible for Visual ChatGPT, Visual ChatGPT should remember to repeat important information in the final response for Human. Thought: Do I need to use a tool?"` as a prefix to the query.

<img width="947" alt="image" src="https://user-images.githubusercontent.com/46675408/228727283-3dc62bfc-bcef-4c23-9cbd-f14792f1e5a6.png">

<img width="596" alt="image" src="https://user-images.githubusercontent.com/46675408/228727306-1c7ffc54-10d0-41ad-9f77-28d3da1b2adc.png">

<img width="646" alt="image" src="https://user-images.githubusercontent.com/46675408/228727346-e260fd19-246a-4f51-abc5-f6c5a5dd3009.png">

<img width="591" alt="image" src="https://user-images.githubusercontent.com/46675408/228727585-d92ddd83-6a49-4788-a863-6bf6c02721aa.png">

<img width="599" alt="image" src="https://user-images.githubusercontent.com/46675408/228727609-0ee2834a-b7d3-47b0-bb77-ab7667d83259.png">


