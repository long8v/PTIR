---
title: "[107] Visual ChatGPT: Talking, Drawing and Editing with Visual Foundation Models"
date: 2023-03-30
tags: ['GPT', '2023Q1']
paper: "https://arxiv.org/pdf/2303.04671.pdf"
issue: 116
issueUrl: "https://github.com/long8v/PTIR/issues/116"
---
<img width="1009" alt="image" src="https://user-images.githubusercontent.com/46675408/228726791-d0115425-a8ee-49d5-962b-3997c632bb14.png">

[paper](https://arxiv.org/pdf/2303.04671.pdf), [github](https://github.com/microsoft/visual-chatgpt), [demo](https://huggingface.co/spaces/microsoft/visual_chatgpt) 

## TL;DR
- **I read this because.. :** GPT 시리즈. 여러 곳에서 회자 되어.
- **task :** chatGPT with visual input output
- **problem :** chatGPT는 언어로만 주고 받는다. 이미지 input / output을 받으면 좋겠다. 그렇다고 chatGPT를 vision model도 받게 하자니 모델 학습하는데 너무 오래걸린다.
- **idea :** 그냥 external Vision Foundation Model들을 call 할 수 있는 시스템을 만들자 -> chain of thought로 어떤 vision model을 call 할건지 thought - action을 하도록 함. -> 채팅 인터페이스에 맞게 애매한 쿼리 재질문하고 만든 이미지 파일을 잘 인용하거나 할 수 있게 시스템을 만듦
- **architecture :** 비전 모델들 hf 등에서 줍줍 + instructGPT 기반의 chatGPT + [LangChain](https://github.com/hwchase17/langchain)을 통해서 시스템 적용 
- **objective :** LM ce loss 
- **baseline :** x 
- **data :** 새로 학습하지 않은 듯 하다
- **evaluation :** qualatatively 
- **result :** 작동
- **contribution :** 최초의? vision chatGPT
- **limitation / things I cannot understand :** flamingo 같은 모델인줄 알았으나 아니었음.. 뭔가 모델이라기 보단 사용설명서 같은 느낌 .. fancy하진 않으나 앞으론 이런 접근법이 대세이려낭..

## Details

<img width="505" alt="image" src="https://user-images.githubusercontent.com/46675408/228727201-c43301c5-fd8a-47fb-a43e-d3b6177e1734.png">

hf에서 visual foundation models + MaskFormer
`Since Visual ChatGPT is a text language model, Visual ChatGPT must use tools to observe images rather than imagination. The thoughts and observations are only visible for Visual ChatGPT, Visual ChatGPT should remember to repeat important information in the final response for Human. Thought: Do I need to use a tool?”`를 prefix로 두고 쿼리를 날렸다고 함. 

<img width="947" alt="image" src="https://user-images.githubusercontent.com/46675408/228727283-3dc62bfc-bcef-4c23-9cbd-f14792f1e5a6.png">

<img width="596" alt="image" src="https://user-images.githubusercontent.com/46675408/228727306-1c7ffc54-10d0-41ad-9f77-28d3da1b2adc.png">

<img width="646" alt="image" src="https://user-images.githubusercontent.com/46675408/228727346-e260fd19-246a-4f51-abc5-f6c5a5dd3009.png">

<img width="591" alt="image" src="https://user-images.githubusercontent.com/46675408/228727585-d92ddd83-6a49-4788-a863-6bf6c02721aa.png">

<img width="599" alt="image" src="https://user-images.githubusercontent.com/46675408/228727609-0ee2834a-b7d3-47b0-bb77-ab7667d83259.png">


