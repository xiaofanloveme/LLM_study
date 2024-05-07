import re
import json
import xml.etree.ElementTree as ET

def extract_invention_title_and_text(xml_content):
    root = ET.fromstring(xml_content)
    namespace = {'business': 'http://www.sipo.gov.cn/XMLSchema/business', 'base': 'http://www.sipo.gov.cn/XMLSchema/base'}
    
    invention_title = root.find('.//business:InventionTitle', namespace)
    abstract = root.find('.//base:Paragraphs[@num="0001"]', namespace)


    text = ''
    for i in range(2, 21):  # Adjusted range to include n20
        paragraph = root.find(f'.//base:Paragraphs[@num="n{i}"]', namespace)
        if paragraph is not None:
            text += paragraph.text

    if invention_title is not None and text:
        return {
            "invention_title": invention_title.text,
            "abstract": abstract.text,
            "text": text
            }
    else:
        return None


# 读取XML文件内容
with open("/home/wrf1/patents/19850910/1/CN101985000005365CN00000851053650BFULZH19850910CN00P/CN101985000005365CN00000851053650BFULZH19850910CN00P.XML", "r", encoding="utf-8") as xml_file:
    xml_content = xml_file.read()

# 提取数据并保存为JSON格式
result = extract_invention_title_and_text(xml_content)
if result:
    with open("patents_data.json", "w", encoding="utf-8") as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=4)
