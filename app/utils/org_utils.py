import re

def generate_org_code(org_name: str, org_id: int) -> str:
    """
    Generate organization code like:
    Baba Travels -> BAB1
    Umrah -> UMR2
    AI -> AIX3
    """
    letters = re.sub(r'[^A-Za-z]', '', org_name).upper()
    prefix = letters[:3] if len(letters) >= 3 else letters.ljust(3, 'X')
    return f"{prefix}{org_id}"
