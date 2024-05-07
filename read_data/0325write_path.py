import os


# 指定目录路径
directory = "/mnt/geogpt-gpfs/llm-course/home/wrf/beifen/1data/out_redpajamawiki.npy"

# 获取目录下以 .npy 结尾的文件路径
file_paths = []
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".npy"):
            file_paths.append(os.path.join(root, file))

# 将文件路径写入txt文件
output_file = "file_paths.txt"
with open(output_file, 'w') as f:
    for path in file_paths:
        f.write("- %s\n" % path)

print("以 .npy 结尾的文件路径已保存到 %s" % output_file)
