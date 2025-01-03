# speed_test.py

import requests
from time import time
from operator import itemgetter
from collections import defaultdict
import os

# 下载live.txt文件并保存到本地
live_file_url = 'https://raw.githubusercontent.com/haotiandao/test2/main/live.txt'
local_live_file = 'live.txt'

try:
    response = requests.get(live_file_url, timeout=10)
    response.raise_for_status()  # 如果请求失败（非200响应），抛出异常
    with open(local_live_file, 'w') as f:
        f.write(response.text.strip())
except Exception as e:
    print(f"Failed to download {live_file_url}: {e}")
    exit(1)  # 退出流程以防止后续步骤继续执行

# 初始化结果列表
results = []

# 测速函数
def test_speed(url):
    try:
        start_time = time()
        response = requests.head(url, timeout=5)  # 使用HEAD请求以减少数据传输量
        response.raise_for_status()  # 确保URL是可访问的
        end_time = time()
        elapsed_time = end_time - start_time
        print(f"Tested {url}: {elapsed_time:.4f} seconds")
        return elapsed_time
    except Exception as e:
        print(f"Failed to test {url}: {e}")
        return None

# 对每个URL进行测速
with open(local_live_file, 'r') as file:
    lines = file.readlines()

for line in lines:
    parts = line.split(',')
    if len(parts) >= 2:
        channel = parts[0].strip()
        url = parts[1].strip()
        if url:  # 确保URL不是空字符串
            speed = test_speed(url)
            results.append((channel, url, speed))

# 将结果按频道分组，并在每组内按速度排序
grouped_results = defaultdict(list)
for channel, url, speed in results:
    grouped_results[channel].append((url, speed))

# 在每个频道内选择最快的速度前20个
top_20_per_channel = {
    channel: sorted(urls, key=lambda x: (x[1] is None, x[1]))[:20]
    for channel, urls in grouped_results.items()
}

# 输出结果到文件
output_file = 'speed-live.txt'
with open(output_file, 'w') as f:
    for channel, urls in top_20_per_channel.items():
        for url, speed in urls:
            f.write(f"{channel},{url}:{speed:.4f} seconds\n" if speed is not None else f"{channel},{url}: Failed\n")

print("Speed test completed and results saved.")
