import transformers
import torch

model_id = "aaditya/OpenBioLLM-Llama3-70B"

pipeline = transformers.pipeline(
    "text-generation",
    model=model_id,
    model_kwargs={"torch_dtype": torch.bfloat16},
    device="auto",
)

async def get_llm_response(messages: list[dict]) -> str:
    prompt = pipeline.tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    terminators = [
        pipeline.tokenizer.eos_token_id,
        pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    outputs = pipeline(
        prompt,
        max_new_tokens=256,
        eos_token_id=terminators,
        do_sample=True,
        temperature=0.0,
        top_p=0.9,
    )

    generated_text = outputs[0]["generated_text"][len(prompt):]
    return generated_text.strip()
