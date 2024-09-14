import os
from openai import OpenAI, AzureOpenAI
from dotenv import load_dotenv



if os.path.exists("/run/secrets/api_keys"):
    load_dotenv("/run/secrets/api_keys")
else:
    load_dotenv("./.env")


def init_openai_client() -> OpenAI | AzureOpenAI:
    """
    Initialize the OpenAI client.
    
    Returns:
    OpenAI | AzureOpenAI: The OpenAI client object.
    """

    if "AZURE_API_KEY" in os.environ:
        return AzureOpenAI(api_key=os.getenv("AZURE_API_KEY"), api_version=os.getenv("AZURE_API_VERSION"), azure_endpoint=os.getenv("AZURE_ENDPOINT"))
    else:
        return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def init_message_history(prompts: dict[dict], mail:str ) -> list[dict[str, str]]:
    """
    Initialize the message history object.
    
    Parameters:
    prompts (dict[dict]): The prompts dictionary.
    position (str): The position of the employee.
    directorate (str): The directorate of the employee.
    category (str): The category of the employee.
    
    Returns:
    MessageHistory: The message history object.
    """


    initial_message_history = [
        {"role": "system", "content": prompts["system"]["text"]},
        {"role": "user", "content": prompts["user"]["text"].format(mail = mail)}
    ]

    return initial_message_history


def extract_info_from_mail(mail: str, client: OpenAI | AzureOpenAI, prompts: dict[dict], model : str = "gpt-3.5-turbo") -> dict[str | None , str, str, str]:
    """
    Extract information from the input mail.
    
    Args:
    mail (str): The input mail.
    client (OpenAI | AzureOpenAI): The OpenAI client object.
    prompts (dict[dict]): The prompts dictionary.
    
    Returns:
    tuple[bool, str]: The flag indicating whether the information was extracted successfully and the extracted information.
    """

    model_name = model
    if isinstance(client, AzureOpenAI):
        model_name = os.getenv("AZURE_DEPLOYMENT_MODEL")
    message_history = init_message_history(prompts, mail)
    completion = client.chat.completions.create(
        model=model_name,
        messages=message_history
    )
    response = completion.choices[0].message.content
    try :

        extract_flag = int(response.split("\n")[0])
    except:
        return {"day": None, "start": None, "end": None, "title": None}
    if extract_flag == 1: 
        day = response.split("\n")[1]
        start = response.split("\n")[2]
        end = response.split("\n")[3]
        title = response.split("\n")[4]
    else:
        day = None 
        start = response.split("\n")[2]
        end = response.split("\n")[3]
        title = response.split("\n")[4]
        
    return {"day": day, "start": start, "end": end, "title": title}
    