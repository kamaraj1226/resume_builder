import os
from langchain_ollama import ChatOllama
from resume_builder.constants import AvailableModel
from pydantic import BaseModel
from typing import Any, List, Dict
from resume_builder.constants import StreamMode
import uuid


def get_ollama_host() -> str:
    host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    return host


def get_ollama_model_name(model_name: AvailableModel) -> str:
    if model_name.name in AvailableModel.__members__:
        return model_name.value
    raise Exception(f"{model_name} is not available")


def get_ollama_model(model_name: str = AvailableModel.qwen_3_5_0_8_b):
    model = ChatOllama(
        model=get_ollama_model_name(model_name=model_name),
        temperature=0.9,
        disable_streaming=False,
    )
    return model


def get_user_input():
    user_input = """
    Here is the job description
    ### start ####
    Job description
Mizuho Global Services Pvt Ltd (MGS) is a subsidiary company of Mizuho Bank, Ltd, which is one of the largest banks or so called 'Mega Banks' of Japan. MGS was established in the year 2020 as part of Mizuho's long-term strategy of creating a captive global processing center for remotely handling banking and IT related operations of Mizuho Bank's domestic and overseas offices and Mizuho's group companies across the globe. At Mizuho we are committed to a culture that is driven by ethical values and supports diversity in all its forms for its talent pool. Direction of MGS's development is paved by its three key pillars, which are Mutual Respect, Discipline and Transparency, which are set as the baseline of every process and operation carried out at MGS.

o Excellent career growth
We are seeking a skilled and vigilant L1 for handling EDR operations to our dynamic security team. The Ideal candidate will play a key role in monitoring, analysing, and responding to security incident. Graduation/Post graduation in, Computers, Information Systems, Computer Science, or Information technology systems
• 5 to 7 years of work experience as security analyst with hands-on experience of EDRs
• Good to have at least one cyber security certification (CEH, CompTIA+ etc.)
• Knowledge of banking business and information technology practices and trends in banking sector
• Ability to communicate effectively, both orally and in writing.
• Should be comfortable for 24/7 shifts

Knowledge and hands-on experience with Carbon black EDR tool, alert detection and response.
• Analyse endpoint data to identify Indicators of compromise (IOCs) and suspicious activities.
• Ability to understand the threat intelligence tool for analysing the alerts in detail.
• Escalate confirmed security incidents to level2 analyst or IR team for further investigations.
• Ensure that all EDR operation and tickets are handled and resolved within SLAs.
• Should have expertise on TCP/IP network traffic, Internet protocols and event log analysis.
• Perform detailed analysis of threats and security events, using analytical skills, knowledge, and experience, with a clear narrative to support conclusions.
• Stayed up with latest cybersecurity threats, vulnerabilities, and trends, particularly those relevant to endpoint.
• Ability to communicate effectively, both orally and in writing.
    ### end ###

    for this job description i want to have a tailored resume.tex file
    You can find my resume in pdf format in this location
    resume_location: /mnt/d/resume_building/resume_builder/files/sample_resume.pdf
    you can find the latex template in the below  mentioned directory
    latex_file_location: /mnt/d/resume_building/resume_builder/files/sample_latex.tex

    Also note that latex template is just the sample none of the content are mine
    You need to use my resume_location (sample_resume.pdf) file and create a new latex file
    That should be tailored and match to my existing resume and job description

    """
    print("\nyou>> ", end="")
    user_input = input()
    print()
    return user_input


class StreamObj(BaseModel):
    agent: Any
    stream_mode: List[str] = [mode.value for mode in StreamMode]
    version: str = "v2"
    config: Dict | Any = {
        "configurable": {"thread_id": str(uuid.uuid4())}
    }  # It is requried for human in the loop conversation
    show_tool_output: bool = True
