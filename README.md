# DeepSeek API Usage

## Memo

发现 deepseek 的 api 接口`function calling`目前无法兼容`openai`的`python`sdk`openai>=1.59.6` 接口。

## 原因

deepseek 的模型在历史messages中如果包含了可能会调用函数的请求，那么在发起新的一轮对话，这个completions如果包含了tools参数，会重复生成调用函数的回复，最早发现是在Swarm的测试中，使用deepseek模型一直无线循环重复生成调用function的回复，使用gpt-4o则没有这个问题。

后来发现是function calling都有这个问题。
