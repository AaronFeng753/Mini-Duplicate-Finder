from hashlib import md5, sha1
from zlib import crc32
from numpy import unique
import time
import sys
import psutil
import binascii
import os
import time
import re


def getCrc32(filename,memory):
	with open(filename, 'rb') as f:
		crc = 0
		while True:
			b = f.read(memory)
			if len(b) == 0:
				break
			crc = binascii.crc32(b, crc)
		return "%08X" %crc

def getMd5(fname,memory):
    hash_md5 = md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(memory), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
    
def getSha1(fname,memory):
    hash_Sha1 = sha1()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(memory), b""):
            hash_Sha1.update(chunk)
    return hash_Sha1.hexdigest()
    
def mainMenu():
	while True:
		print('Mini duplicate finder v0.1')
		print('---------------------------------')
		print('A: Duplicate finder')
		print('B: Check files(MD5,SHA1,CRC32)')
		print('----------------------------------')
		mode = input('(a/b) : ')
		if mode.lower() == "a":
			os.system('cls')
			duplicateFinder()
			os.system('cls')
		elif mode.lower() == "b":
			os.system('cls')
			checkFile()
			os.system('cls')
		else:
			os.system('cls')
			input('Error : wrong input,pls press any key to return')
			os.system('cls')

def findDuplictaeFile(inputPath):
	pc_mem = psutil.virtual_memory()
	memory = int(pc_mem.available/10)
	fileList=[]
	fileAndSha1={}
	duplicateFile={}
	subFolder='Y'
	
	for path in os.walk(inputPath):
		if path[1]!=[]:
			subFolder=input('Scan subfolders?(y/n) :')
			subFolder=subFolder.upper()
		break
		
	print('')
	sys.stdout.write('\r Processing....')
	sys.stdout.flush()
	
	for path,useless,files in os.walk(inputPath):
		for filename in files:
			fileList.append(path+'\\'+filename)
		if subFolder=='N':
			break
	
	for file_ in fileList:
		size = os.path.getsize(file_)
		sha1_localFile=''
		if size < memory:
			sha1_localFile=getSha1(file_,size).upper()
		else:
			sha1_localFile=getSha1(file_,memory).upper()
		fileAndSha1[file_]=sha1_localFile
		
	for key_1,value_1 in fileAndSha1.items():
		for key_2,value_2 in fileAndSha1.items():
			if (value_1==value_2) & (key_1 != key_2):
				duplicateFile[value_1]=[]
	
	for key_1,value_1 in fileAndSha1.items():
		for key_2,value_2 in fileAndSha1.items():
			if (value_1==value_2) & (key_1 != key_2):
				duplicateFile[value_1].append(key_2)
				
	for key,value in duplicateFile.items():
		duplicateFile[key]=unique(value)
	
	sys.stdout.write('\r Complete!       ')
	sys.stdout.flush()
	
	return duplicateFile

def duplicateFinder():
	
	inputPath = input('Path:')
	inputPath = inputPath.strip('"')
	
	duplicateFile=findDuplictaeFile(inputPath)
		
	sys.stdout.write('\r Complete!       \n')
	sys.stdout.flush()
	
	for value in duplicateFile.values():
		print('======================================')
		NumOfFile = 0
		for file_ in value:
			print('[',NumOfFile,'] --- ',file_)
			NumOfFile=NumOfFile+1
		print('======================================')
		
	print('\n======================================')
	print('A: Delete extra files automatically.')
	print('B: Delete extra files manually.')
	print('C: Don\'t Delete extra files.')
	print('======================================')
	delFileorNot=input('(A/B/C):')
	delFileorNot=delFileorNot.upper()
	
	if delFileorNot == 'A':
		print('')
		for key,value in duplicateFile.items():
			for path in range(1,len(value)):
				print('Delete '+value[path])
				os.remove(value[path])
		input('\nPress any key to return to the main menu')
				
	elif delFileorNot == 'B':
		os.system('cls')
		ManualDel(duplicateFile)
		print('\nManual delete complete')
		input('Press any key to return to the main menu')
			
def ManualDel(duplicateFile):
	DuplicateFilePair_max = len(duplicateFile)
	DuplicateFilePair_min = 1
	for value in duplicateFile.values():
		while True:
			print('Duplicate File Pair: (',DuplicateFilePair_min,'/',DuplicateFilePair_max,')')
			DuplicateFilePair_min = DuplicateFilePair_min+1
			print('======================================')
			NumOfFile = 0
			for file_ in value:
				print('[',NumOfFile,'] --- ',file_)
				NumOfFile=NumOfFile+1
			print('======================================')
			print('Enter the number of the files you wanna delete.')
			print('For example: 0/2/3')
			print('If you don\'t wanna delete any file, just press \'Enter\'')
			delfile = input()
			if delfile == '':
				os.system('cls')
				break
			else:
				pattern = re.compile(r'\d+/\d+|\d+')
				if pattern.match(delfile) != None:
					delfile=delfile.split('/',-1)
					for No in delfile:
						os.remove(value[int(No)])
					os.system('cls')
					break
				elif pattern.match(delfile) == None:
					print('Wrong input!')
					input()
				
	
def checkFile():
	pc_mem = psutil.virtual_memory()
	memory = int(pc_mem.available/10)

	filename = input('File(path and name):')
	filename=filename.strip('"')
	print('')
	sys.stdout.write('\r Processing....')
	sys.stdout.flush()
	
	size = os.path.getsize(filename)
	if size < memory:
		memory=size
	
	md5_localFile=getMd5(filename,memory).upper()
	sha1_localFile=getSha1(filename,memory).upper()
	crc32_localFile=getCrc32(filename,memory).upper()
	
	sys.stdout.write('\r Complete!       ')
	sys.stdout.flush()
	print('')
	print('\nMD5: ', md5_localFile)

	print('SHA1: ', sha1_localFile)
	
	print('CRC32: ', crc32_localFile)
	
	input('\nPress any key to return to the main menu')
	
mainMenu()
	


