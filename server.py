import yaml
from utils import init_openai_client, extract_info_from_mail


openai_client = init_openai_client()

with open("./prompts.yaml", "rb") as f:
    prompts = yaml.safe_load(f)
    



def extract(mail: str) -> dict[str, any]:
    """
    Classify the input text.
    
    Args:
    input_body (InputBody): The input text.
    
    Returns:
    dict[str, any]: The classification result.
    """

    try: 
        response = extract_info_from_mail(mail,openai_client,prompts)
        if response['day'] == None :
            response['day'] = None
        elif "None" in response['day'] : 
            response['day'] = None
        elif len(response['day'].split("-") ) != 3 :
            response['day'] = None
    
    except:
        response = {"day": None, "start": None, "end": None, "title": None}


    return response

