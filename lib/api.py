import sys
sys.path.append('..')
from .translator import PaperTranslator
from SETTINGS import *

def translate_api(src_text):

	machine = PaperTranslator(appid=APPID, secretKey=KEY, url=URL)
	lines = src_text.split('\n')
	dst_text = ""
	batch = ''
	cnt = 0
	for line in lines:
		line = line.strip()
		if len(line) == 0:
			if len(batch)!=0:
				cnt += 1
				dst_text += machine.translate(batch) + '\n\n'

			batch = ''
		else:
			batch += ' ' + line

	if batch:
		dst_text += machine.translate(batch) + '\n\n'
			
	return dst_text
