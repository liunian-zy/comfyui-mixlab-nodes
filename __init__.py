#
import os
import subprocess
import importlib.util
import sys,json
import execution
import uuid
import hashlib
import datetime
import folder_paths
import logging
import base64,io,re
import random
from PIL import Image
from comfy.cli_args import args
python = sys.executable

#修复 sys.stdout.isatty()  object has no attribute 'isatty'
try:
    sys.stdout.isatty()
except:
    print('#fix sys.stdout.isatty')
    sys.stdout.isatty = lambda: False

_URL_=None


current_path = os.path.abspath(os.path.dirname(__file__))




# 种子设置
def random_seed(seed, data):
    max_seed = 4294967295

    for id, value in data.items():
        # print(seed,id)
        if id in seed:
            if 'seed' in value['inputs'] and not isinstance(value['inputs']['seed'], list) and seed[id] in ['increment', 'decrement', 'randomize']:
                value['inputs']['seed'] = round(random.random() * max_seed)
            
            if 'noise_seed' in value['inputs'] and not isinstance(value['inputs']['noise_seed'], list) and seed[id] in ['increment', 'decrement', 'randomize']:
                value['inputs']['noise_seed'] = round(random.random() * max_seed)
            
            if value.get('class_type') == "Seed_" and seed[id] in ['increment', 'decrement', 'randomize']:
                value['inputs']['seed'] = round(random.random() * max_seed)
            
        print('new Seed', value)
    
    return data


# 导入节点
from .nodes.ImageNode import SaveImageAndMetadata
from .nodes.Utils import MultiplicationNode

# 要导出的所有节点及其名称的字典
# 注意：名称应全局唯一
NODE_CLASS_MAPPINGS = {
    
    "SaveImageAndMetadata_":SaveImageAndMetadata,
    "MultiplicationNode": MultiplicationNode,

}

# 一个包含节点友好/可读的标题的字典
NODE_DISPLAY_NAME_MAPPINGS = {
   
    "SaveImageAndMetadata_":"Save Image Output ♾️MixlabApp",
    "MultiplicationNode": "Math Operation ♾️Mixlab",

}

# web ui的节点功能
WEB_DIRECTORY = "./web"

logging.info('--------------')
logging.info('\033[91m ### Mixlab Nodes: \033[93mLoaded')
# print('\033[91m ### Mixlab Nodes: \033[93mLoaded')


logging.info('\033[93m -------------- \033[0m')
