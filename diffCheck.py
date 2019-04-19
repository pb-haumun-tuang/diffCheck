# coding: utf-8

import tarfile
import os
import sys

if not len(sys.argv) == 3:
	exit()

tar1 = sys.argv[1]
tar2 = sys.argv[2]

#　○○なら変更点ないと決めるため
standard_diff = 2.0

print('checking ...............')

# 2つのtarの中身（構成）を辞書型に入れる
def create_dict(extractedTar, targetDict):
	for idx, data in enumerate(extractedTar.getmembers()):
		targetDict.update(
			{
				data.name:{
					'type': 'file' if data.isfile() else 'dir',
					'size':data.size,
				}
			}
		)
		
		#if targetDict[data.name]['type'] == '' and targetDict[data.name]['size'] == 0:
		#	del targetDict[data.name]

def is_same(arg_1, arg_2):
	# 2っのdictにあるkey(file path)をunionする
	union_keys = set().union(list(arg_1.keys()), arg_2.keys())
	for union_key in union_keys:
		if arg_1.get(union_key) == None:
			print(union_key+' is missing in arg_1 \n')
			continue
		if arg_2.get(union_key) == None:
			print(union_key+' is missing in arg_2 \n')
			continue
		if arg_1[union_key]['size'] != arg_2[union_key]['size']:
			diff_rate = (abs((arg_1[union_key]['size']-arg_2[union_key]['size']))/((arg_1[union_key]['size']+arg_2[union_key]['size'])/2))*100
			if not round(standard_diff-diff_rate) == round(standard_diff):
				print('size not match: '+ union_key)
				print('arg_1: '+str(arg_1[union_key]['size']))
				print('arg_2: '+str(arg_2[union_key]['size']))
				print('Diff Rate: '+str(round(diff_rate, 3))+'%'+'\n')


dict_tar1 = {}
dict_tar2 = {}

create_dict(tarfile.open(tar1), dict_tar1)
create_dict(tarfile.open(tar2), dict_tar2)

is_same(dict_tar1, dict_tar2)
