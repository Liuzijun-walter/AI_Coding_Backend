import asyncio

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from params import *
from llm_utils import stream_llm_response

from prompts.code_assistant import *

router = APIRouter()

@router.post('/api/explain')
async def explain(body: NaiveChatRequest):
    context = body.context
    return StreamingResponse(stream_llm_response(
        prompt_template=chat_prompt,
        input_variables={
            'context': context,
        },
        print_prompts=False,
        print_response=True,
    ))
    