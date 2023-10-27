import bs4
import re

def get_html_text(html):
    try:
        return bs4.BeautifulSoup(html, 'lxml').body.get_text(' ', strip=True)
    except AttributeError: # message contents empty
        return None
    
def sanitize_text(text:str) -> str:
    return text.replace('-','').replace('\t','').replace('_','').replace('*','')

def is_email(text):
    local_text = text.replace(' ','').replace('\t','')
    expr = re.search("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.){1}(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$",local_text)
    return expr