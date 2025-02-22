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
    url = "https://google.serper.dev/search"
    query = f"homepage of {author_name}, a researcher on computer science"

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

            # 优先寻找包含"homepage"或"个人主页"的链接
            for result in results[:5]:  # 检查前5个结果
                link = result.get('link', '')
                if any(keyword in link.lower() for keyword in ["~", "homepage", "personal"]):
                    return link

            # 如果没有明显主页特征，返回第一个结果
            return results[0].get('link') if results else None

    except Exception as e:
        print(f"搜索失败: {str(e)}")
        return None
