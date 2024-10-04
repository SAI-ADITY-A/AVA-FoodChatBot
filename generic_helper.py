import re

def extract_session_id(session_str: str):
    match = re.search(r"/sessions/(.*?)/contexts/", session_str)
    if match:
        extracted_str = match.group(1) 
        return extracted_str
    
    return ""

def get_str_food_dict(food_dict: dict):
    return ", ".join([f"{int(value)} {key}" for key, value in food_dict.items()])

if __name__ == "__main__":
    print(get_str_food_dict({'samosa': 2, 'lassi': 1}))
    print(extract_session_id("projects/ava-chatbot-wtxo/agent/sessions/af214100-8ecf-cf9d-8dc4-a11f389a0b65/contexts/ongoing-order"))