
# -*- coding=utf-8
# platform
import platform
plat = platform.system().lower()
if plat == 'windows':
    seg = '\\'
elif plat == 'linux' or plat =='darwin': # linux or macOS
    seg = '/'
else:
    raise NotImplementedError

# appid 已在配置中移除,请在参数 Bucket 中带上 appid。Bucket 由 BucketName-APPID 组成
# 1. 设置用户配置, 包括 secretId，secretKey 以及 Region
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import os.path as osp
import glob
import argparse
import logging
import pickle
import re 
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
secret_id = ''      # 替换为用户的 secretId(登录访问管理控制台获取)
secret_key = ''      # 替换为用户的 secretKey(登录访问管理控制台获取)
region = 'ap-beijing'     # 替换为用户的 Region
bucket = '' # 替换为用户存储桶名称
token = None                # 使用临时密钥需要传入 Token，默认为空，可不填
scheme = 'https'            # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
# 2. 获取客户端对象
client = CosS3Client(config)
# 参照下文的描述。或者参照 Demo 程序，详见 https://github.com/tencentyun/cos-python-sdk-v5/blob/master/qcloud_cos/demo.py

def uploadSingle(file_path, target_path=None):
    if target_path is None:
        target_path = file_path.split(seg)[-1]
    with open(file_path, 'rb') as fp:
        response = client.put_object(
            Bucket=bucket,
            Body=fp,
            Key=target_path,
            StorageClass='STANDARD',
            EnableMD5=False
        )
    url = 'https://{}.cos.{}.myqcloud.com/{}'.format(bucket, region, target_path)
    return {target_path: url}

def deleteSingle(target_path):
    response = client.delete_object(
            Bucket=bucket,
            Key=target_path,
        )


def uploadFolder(folder_path):
    # 获取foloder下面的文件列表
    file_paths = glob.glob(osp.join(folder_path, '*'))
    if len(file_paths) == 0:
        return {}
    # 获取直接目录
    direct_dir = file_paths[0].split(seg)[-2]
    # 上传文件，返回url
    urls = {}
    for file_path in file_paths:
        file_name = file_path.split(seg)[-1]
        url = uploadSingle(file_path, direct_dir+'/'+file_name)
        urls.update(url)
    return urls


def deleteFolder(folder_path):
    # 获取foloder下面的文件列表
    file_paths = glob.glob(osp.join(folder_path, '*'))
    # 获取直接目录
    direct_dir = folder_path.split(seg)[-1]
    for file_path in file_paths:
        file_name = file_path.split(seg)[-1]
        deleteSingle(direct_dir+'/'+file_name)
    
def queryBucket(prefix=''):
    marker = ""
    while True:
        response = client.list_objects(
            Bucket=bucket,
            Prefix=prefix,
            Marker=marker
        )
        for item in response['Contents']:
            print(item['Key'])
        if response['IsTruncated'] == 'false':
            break 
        marker = response['NextMarker']


def replace(urls, file_name, output_file_name):

    f = open(file_name, 'r')
    f_output = open(output_file_name, 'w')
    lines = f.read()
    for local_img_path, url in urls.items():
        pattern = r"!\[(.*?)\]\(" + local_img_path + r"\)"
        new_pattern = r"![\1](" + url + r")"
        lines = re.sub(pattern, new_pattern, lines)
    f_output.write(lines)
    f.close()
    f_output.close()
   

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('op', choices=['u', 'd', 'q'], type=str)
    parser.add_argument('--dir', type=str, default=None, help='upload a folder')
    parser.add_argument('--img', type=str, default=None, help='upload a file')
    parser.add_argument('--doc', type=str, default=None, help='upload a file')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    if args.op == 'u':
        if args.dir:
            urls = uploadFolder(args.dir)
        
        if args.img:
            urls = uploadSingle(args.img)
        
        if args.doc:
            suffix = args.doc.split('.')[1]
            replace(urls, args.doc, args.doc.split('.')[0]+'_urls.'+suffix)

    elif args.op == 'd':
        if args.dir:
            deleteFolder(args.dir)
        if args.file:
            deleteSingle(args.img)
    elif args.op == 'q':
        queryBucket()
