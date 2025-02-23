import requests
import os
from utils import read_data

def download_file(url, save_path):
    try:
        # 发送HTTP GET请求获取文件内容
        response = requests.get(url, stream=True)
        # 检查响应状态码，如果不是200则抛出异常
        response.raise_for_status()

        # 以二进制写入模式打开文件
        with open(save_path, 'wb') as file:
            # 遍历响应内容的每个数据块
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    # 将数据块写入文件
                    file.write(chunk)
        print(f"文件 {save_path} 下载成功")
    except requests.RequestException as e:
        print(f"下载文件时发生错误: {e}")
    except Exception as e:
        print(f"发生未知错误: {e}")

def batch_download_files(urls, save_dir):
    # 如果保存目录不存在，则创建该目录
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 遍历每个URL
    for url in urls:
        # 从URL中提取文件名
        file_name = os.path.basename(url+'.pdf')
        # 拼接保存文件的完整路径
        save_path = os.path.join(save_dir, file_name)
        # 调用下载文件的函数
        download_file(url, save_path)

if __name__ == "__main__":
    # 定义要下载的文件的URL列表
    papers = read_data('./data/combined_result.csv')
    file_urls = [
        # "https://arxiv.org/pdf/2401.01335",
        # "https://arxiv.org/pdf/2310.10631"
    ]
    for paper in papers:
        url = paper.url
        if 'arxiv.org' in url:
            url = url.replace('/abs/','/pdf/')
            file_urls.append(url)
    
    # 定义保存文件的目录
    save_directory = "./downloads"
    # 调用批量下载函数
    batch_download_files(file_urls, save_directory)