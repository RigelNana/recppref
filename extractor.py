from bs4 import BeautifulSoup
from bs4.element import Tag
import tqdm
import os
import re

with open('cppref.xml', 'r') as file:
    content = file.read()

soup = BeautifulSoup(content, 'lxml')

pages = soup.find_all('page')
for page in tqdm.tqdm(pages, desc="Processing pages"):
    title: str = page.find('title').text
    title = title.replace(" ", "_")

    with open('titles.txt', 'a') as f:
        f.write(title + '\n')
    if title.startswith("cpp"):
        
        # 直接从原始XML中提取text标签的内容，保持HTML实体不变
        page_str = str(page)
        # 使用正则表达式提取<text>标签中的原始内容
        text_match = re.search(r'<text[^>]*>(.*?)</text>', page_str, re.DOTALL)
        if text_match:
            text: str = text_match.group(1)
        else:
            text: str = ""
        
        # something like cpp/algorithm/accumulate, create a template file
        filepath = f'wikis/{title}.wiki'
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            f.write(text)
        
