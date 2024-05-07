import xml.etree.ElementTree as ET

prefix = "{http://www.sipo.gov.cn/XMLSchema/business}"
file_name = "CN112018000093109CN00001120885560BFULZH20220104CN002.XML"
file_name = "CN112018000095295CN00001123690680BFULZH20220104CN00O.XML"
file_name = "CN112022000001564CN00001151520300BFULZH20230630CN00U.XML"


def parse_from_xml(file_path):
    tree = ET.parse(file_name)
    root = tree.getroot()

    def get_text(iter, skip=0):
        result = ""
        for each in iter:
            if skip:
                skip -= 1
                continue
            text = each.text.strip()
            if text:
                result += (each.text + "\n")
        return result[:-1]

    k_v_dict = {}
    # 摘要
    abstract = root.find(f"{prefix}Abstract")
    abstract_text = get_text(abstract)
    k_v_dict["abstract"] = abstract_text.strip()

    description = root.find(f"{prefix}Description")
    # 标题
    title = description.find(f"{prefix}InventionTitle")
    k_v_dict["title"] = title.text
    # 技术领域
    technical_field = description.find(f"{prefix}TechnicalField")
    technical_field_text = get_text(technical_field, 1)
    k_v_dict["technical_field"] = technical_field_text
    # 技术背景
    background = description.find(f"{prefix}BackgroundArt")
    background_text = get_text(background, 1)
    k_v_dict["background"] = background_text
    # 发明内容
    disclosure = description.find(f"{prefix}Disclosure")
    disclosure_text = get_text(disclosure, 1)
    k_v_dict["disclosure"] = disclosure_text
    # 具体实施例
    invention_mode = description.find(f"{prefix}InventionMode")
    invention_mode_text = get_text(invention_mode, 1)
    k_v_dict["inventionMode"] = invention_mode_text
    # 权利要求点
    claims = root.find(f"{prefix}Claims")
    claims_text = []
    for each in claims:
        claims_text.append(get_text(each))
    k_v_dict["claims"] = claims_text

    return k_v_dict


result = parse_from_xml(file_name)
for k,v in result.items():
    print(k)
    print(v)
    print("*"*10)