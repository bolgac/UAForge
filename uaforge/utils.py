import string
import random
from typing import List

def save_useragents_to_file(useragents: List[str], filename: str = None):
    """
    Save a list of user agents to a text file.
    Args:
        useragents (List[str]): A list of user agent strings to save.
        filename (str, optional): The name of the file to save to. If None, a random filename
                                  with format "user_agent_<12_digits>.txt" will be generated.
                                  Defaults to None.
    Returns:
        str: The filename where the user agents were saved.
    Example:
        >>> uas = ["Mozilla/5.0...", "Chrome/91.0..."]
        >>> save_useragents_to_file(uas)
        'user_agent_123456789012.txt'
        >>> save_useragents_to_file(uas, "my_agents.txt")
        'my_agents.txt'
    """

    if filename is None:
        random_str = ''.join(random.choices(string.digits, k=12))
        filename = f"user_agent_{random_str}.txt"
    
    with open(filename, "w", encoding="UTF-8") as file:
        for ua in useragents:
            file.write(f"{ua}\n")
    
    return filename
