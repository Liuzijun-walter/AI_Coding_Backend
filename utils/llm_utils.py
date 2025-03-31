import uuid

from langchain_core.prompts import PromptTemplate
from langchain_ollama.llms import Ollama


llm = Ollama(
    model="deepseek-coder:33b",
    temperature=0
)

def pretty_prompt(prompt_template: str, input_variables: dict) -> str:
    if not input_variables or len(input_variables) == 0:
        return prompt_template
    try:
        return str.format(prompt_template, **input_variables)
    except Exception as e:
        dict_str = '\n'.join([f'{key}: {value}' for key, value in input_variables.items()])
        return f'{prompt_template}\n\n{dict_str}'

async def stream_llm_response(
        prompt_template: str,
        input_variables: dict,
        print_prompts=True,
        print_response=True,
        tag=None
):
    """
    生成器函数： 返回LLM生成结果
    """
    uid = tag + '-' + str(uuid.uuid4()) if tag else uuid.uuid4()

    try:
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=[key for key in input_variables.keys()]
        )
        if print_prompts:
            print(f'>>>>>>>>>>>>>>>>>>>>\n{uid}\n\n<<<<<<<<<<<<<<<<<<<\n{pretty_prompt}')
        if print_response:
            print('>>>>>>>>>>>') if not print_prompts else None

        async for chunk in llm.astream(prompt.format(**input_variables), user=uid):
            if print_response:
                print(chunk.context, end='', flush=True)
            yield chunk.content
        
        if print_prompts:
            print('\n<<<<<<<<<<<<<<<<<<')
    except Exception as e:
        print(f'Error in LLM response: {e}')
        raise RuntimeError(f'[LLMCallError]: stream_llm_response failed\n{e}')
            
        