import os
import re
from openai import OpenAI
from stream_bench.llms.base import LLM
from .utils import retry_with_exponential_backoff

class MiniMaxChat(LLM):
    def __init__(self, model_name='MiniMax-M2.5') -> None:
        self.client = OpenAI(
            api_key=os.environ['MINIMAX_API_KEY'],
            base_url="https://api.minimax.io/v1"
        )
        self.model_name = model_name

    @retry_with_exponential_backoff
    def __call__(self, prompt: str, max_tokens: int = 1024, temperature=0.0, **kwargs) -> tuple[str, dict]:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{'role': 'user', 'content': prompt}],
            temperature=float(temperature),
            max_tokens=int(max_tokens),
            extra_body={"thinking_mode": "off"},
        )
        res_text = response.choices[0].message.content or ""
        res_text = re.sub(r"<think>.*?</think>", "", res_text, flags=re.DOTALL).strip()
        res_info = {
            "input": prompt,
            "output": res_text,
            "num_input_tokens": response.usage.prompt_tokens,
            "num_output_tokens": response.usage.completion_tokens,
            "logprobs": []
        }
        return res_text, res_info
