import numpy as np

# 用'rb'模式打开文件以二进制读取
path0 = '/mnt/geogpt-gpfs/llm-course/home/wrf/beifen/1data/out_redpajamastackexchange.npy/0716_00000.npy'

with open(path0, 'rb') as f:
    data = np.fromfile(f, dtype= np.uint16)  # 假设数据类型为float64/32/bool_，根据实际情况修改


print(data[3000:3200])
# 打印数组的形状
print("Shape:", data.shape)