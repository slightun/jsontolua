
import json
import types
import json
import os
import getopt
import sys

def space_str(layer):
	spaces = ""
	for i in range(0, layer):
		spaces += '\t'
	return spaces

def dic_to_lua_str(data,layer=0):
	if isinstance(data, str) :
		yield ("\"" + data + "\"")
	elif isinstance(data, bool):
		if data:
			yield ('true')
		else:
			yield ('false')
	elif isinstance(data, int) or isinstance(data, float):
		yield (str(data))
	elif isinstance(data, list):
		yield ("{\n")
		yield (space_str(layer + 1))
		for i in range(0, len(data)):
			for sub in  dic_to_lua_str(data[i], layer + 1):
				yield sub
			if i < len(data)-1:
				yield (',')
		yield ('\n')
		yield (space_str(layer))
		yield ('}')
	elif isinstance(data, dict):
		yield ("\n")
		yield (space_str(layer))
		yield ("{\n")
		data_len = len(data)
		data_count = 0
		for k,v in data.items():
			data_count += 1
			yield (space_str(layer + 1))
			if isinstance(k, int):
				yield ('[' + str(k) + ']')
			else:
				yield (k) 
			yield (' = ')
			try:
				for sub in  dic_to_lua_str(v,layer + 1):
					yield sub
				if data_count < data_len:
					yield (',\n')

			except Exception as e:
				print('error in ', k, v)
				raise
		yield ('\n')
		yield (space_str(layer))
		yield ('}')
	else:
		raise(d_type , 'is error')

def str_to_lua_table(jsonStr):
	data_dic = None
	try:
		data_dic = json.loads(jsonStr)
	except Exception as e:
		data_dic = []
	else:
		pass
	finally:
		pass
	bytes = ''
	for it in dic_to_lua_str(data_dic):
		bytes += it
	return bytes

def file_to_lua_file(jsonFile, luaFile):
	with open(luaFile,'w') as luafile:
		with open(jsonFile) as jsonfile:
			luafile.write(str_to_lua_table(jsonfile.read()))

if __name__ == "__main__" :
	opts, args = getopt.getopt(sys.argv[1:],'-i:-o:',['input','output'])
	jsonFile = None
	luaFile = None
	for opt_name, opt_value in opts:
		if opt_name in ('-i','--input'):
			jsonFile = opt_value
		if opt_name in ('-o','--output'):
			luaFile = opt_value
	if not jsonFile:
		print("[error] no input file with param -i")
		exit()
	if not luaFile:
		print("[error] no output file with param -o")
		exit()

	#file_to_lua_file("DT_CustomEquip.json", "DT_CustomEquip.lua")
	file_to_lua_file(jsonFile, luaFile)

	# python jsontolua.py -i DT_CustomEquip.json -o DT_CustomEquip.lua