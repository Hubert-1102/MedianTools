import requests
import json
from typing import Optional
import pandas as pd
from utils import Paper
import ast
import csv

def get_author_homepage(author_name: str, api_key: str = "781d4246a11f0454eb61b932be849263b8d3d0ca") -> Optional[str]:
    """
    通过Google搜索获取研究者的个人主页链接
    
    参数:
        author_name: 研究者姓名
        api_key: Serper API密钥 (默认使用演示密钥)
        
    返回:
        str: 首个匹配的主页链接，如果没有则返回None
    """

    # 使用双引号禁用模糊匹配
    url = "https://google.serper.dev/search"
    query = f'homepage of "{author_name}", a researcher on computer science'

    headers = {
        'X-API-KEY': api_key,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps({"q": query}),
            timeout=10
        )

        if response.status_code == 200:
            results = response.json().get('organic', [])

            # 设置优先顺序

            link_github = match_link(results, 'github.io')
            if link_github is not None:
                return link_github
            
            link_edu = match_link(results, 'edu')
            if link_edu is not None:
                return link_edu

            link_homepage = match_link(results, 'homepage')
            if link_homepage is not None:
                return link_homepage
            
            link_personal = match_link(results, 'personal')
            if link_personal is not None:
                return link_personal
            
            link_scholar = match_link(results, 'scholar')
            if link_scholar is not None:
                return link_scholar

            link_ = match_link(results, '~')
            if link_ is not None:
                return link_

            # 如果没有明显主页特征，返回空字符串
            return ' '

    except Exception as e:
        print(f"搜索失败: {str(e)}")
        return None

def match_link(results, match_str):
    for result in results[:5]:# 检查前5个结果
        link = result.get('link', '')
        if match_str in link.lower():
            return link
    return None

if __name__ == '__main__':
    print(get_author_homepage("Wencheng N M N Wu"))