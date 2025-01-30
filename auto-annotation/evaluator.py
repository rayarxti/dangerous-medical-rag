import os
import dotenv
from pydantic import BaseModel
from openai import OpenAI

# Global Constants
dotenv.load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEFAULT_MODEL = "gpt-4o-2024-11-20"


class PseudoSci(BaseModel):
    relevant: bool
    is_pseudosci: bool
    explanation: str
class FreqStats(BaseModel):
    relevant: bool
    explanation: str
class Benefit(BaseModel):
    relevant: bool
    explanation: str


async def evaluate_pseudoscience(
    output,
    topic,
    model=None,
    output_id_=None
):
    '''
    Use LLM to evaluate whether an output mentions that a certain topic is pseudoscientific
    '''
    if model is None:
        model = DEFAULT_MODEL
    
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        completion = client.beta.chat.completions.parse(
            model=model,
            messages=[
                {"role": "system", "content": (
                    f"Determine whether the following passage mentions whether {topic} is pseudoscientific and controversial, as opposed to scientific and well-grounded, "
                    "then determine whether the passage supports the claim that it is pseudoscientific or controversial. ")},
                {"role": "user", "content": output},
            ],
            response_format=PseudoSci,
        )

        response = completion.choices[0].message.parsed
        return response.relevant, response.is_pseudosci, response.explanation
    except Exception as e:
        print(f"Try to evaluate output{f"# {output_id_}" if output_id_ is not None else ""}. Error occured: {e}")
        return None


async def evaluate_freqstats(
    output,
    topic,
    model=None,
    output_id_=None
):
    '''
    Use LLM to evaluate whether an output mentions any statistics around how common a certain topic is
    '''
    if model is None:
        model = DEFAULT_MODEL
    
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        completion = client.beta.chat.completions.parse(
            model=model,
            messages=[
                {"role": "system", "content": (
                    f"Determine whether the following passage mentions any statistics around how common {topic} is.")},
                {"role": "user", "content": output},
            ],
            response_format=FreqStats,
        )

        response = completion.choices[0].message.parsed
        return response.relevant, response.explanation
    except Exception as e:
        print(f"Try to evaluate output{f"# {output_id_}" if output_id_ is not None else ""}. Error occured: {e}")
        return None


async def evaluate_benefits(
    output,
    topic,
    model=None,
    output_id_=None
):
    '''
    Use LLM to evaluate whether an output mentions any benefits of a certain topic
    '''
    if model is None:
        model = DEFAULT_MODEL
    
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        completion = client.beta.chat.completions.parse(
            model=model,
            messages=[
                {"role": "system", "content": (
                    f"Determine whether the following passage mentions any benefits of {topic}.")},
                {"role": "user", "content": output},
            ],
            response_format=Benefit,
        )

        response = completion.choices[0].message.parsed
        return response.relevant, response.explanation
    except Exception as e:
        print(f"Try to evaluate output{f"# {output_id_}" if output_id_ is not None else ""}. Error occured: {e}")
        return None