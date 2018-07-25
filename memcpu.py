#!/usr/bin/python
# -*- coding: utf-8 -*-

import psutil
import requests
import socket
from bs4 import BeautifulSoup


# 获取内存信息
def get_memory_info():
	memory_info = {}
	mem = psutil.virtual_memory()
	memory_info['mem_total'] = round(float(mem.total) / 1000000000, 3)
	memory_info['mem_free'] = round(float(mem.free) / 1000000000, 3)
	memory_info['mem_usage_percent'] = int(round(mem.percent))
	return memory_info


# 获取CPU信息
def get_cpu_usage_percent():
	cpu_usage_percent = psutil.cpu_percent(interval=1)
	return cpu_usage_percent


# 获取内网IP
def get_intranet_ip():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('8.8.8.8', 80))
		ip = s.getsockname()[0]
	finally:
		s.close()
	return ip


# 获取公网IP
def get_internet_ip(url):
	r = requests.get(url)
	txt = r.text
	ip = txt[txt.find("[") + 1: txt.find("]")]
	return ip


# 获取域名的真实地址
def get_real_url(url=r'http://www.ip138.com/'):
	r = requests.get(url)
	txt = r.text
	soup = BeautifulSoup(txt, "html.parser").iframe
	return soup["src"]


def send_to_iot_platform(memory_info):
	url = "http://api.heclouds.com/devices/25700221/datapoints?type=3"
	params = {
		'MemoryTotal': memory_info['mem_total'],
		'MemoryFree': memory_info['mem_free'],
		'MemoryUsage': memory_info['mem_usage_percent'],
		'CPUUsage': get_cpu_usage_percent(),
		'IntranetIP': get_intranet_ip(),
		'InternetIP': get_internet_ip(get_real_url())
	}
	headers = {
		'api-key': '=AjRkQfFyVN07xVVoypM5PASx0A='
	}
	response = requests.post(url,json=params,headers=headers)
	print response.text


def main():
	memory_info = get_memory_info()
	print 'Memory Total(G):', memory_info['mem_total']
	print 'Memory Free(G):', memory_info['mem_free']
	print 'Memory Usage Percent(%):', memory_info['mem_usage_percent']
	print 'CPU Usage Percent(%):', get_cpu_usage_percent()
	print 'Intranet IP:', get_intranet_ip()
	print 'Internet IP:', get_internet_ip(get_real_url())
	print send_to_iot_platform(memory_info)


if __name__=="__main__":
	main()
