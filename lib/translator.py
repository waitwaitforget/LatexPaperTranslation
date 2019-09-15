import sys
import hashlib
import requests
import urllib.parse
import urllib.request
import json
import random

import re

class Translator(object):
	"""docstring for Translator
	
		General translator for common text.
	"""
	def __init__(self, appid, secretKey, url, fromLang='en', toLang='zh'):
		super(Translator, self).__init__()
		self.appid = appid
		self.secretKey = secretKey
		self.fromLang = fromLang
		self.toLang = toLang
		self.url = url
		
	def translate(self, src):
		'''
		modified from baidu translation demo code
		@args:
		src: src text
		@return:
		ret_res: translated text
		'''
		salt = random.randint(32768, 65536)
		sign = self.appid + src + str(salt) + self.secretKey
		
		hl = hashlib.md5()
		hl.update(sign.encode(encoding='utf-8'))
		sign = hl.hexdigest()

		req_url = self.url+'?appid=' + self.appid+'&q='+urllib.parse.quote(src)+'&from='+self.fromLang+'&to='+self.toLang+'&salt='+str(salt)+'&sign='+sign
		response = requests.get(req_url)
		result = json.loads(response.text)
		
		ret_res = ' '.join(result['trans_result'][i]['dst'] for i in range(len(result['trans_result'])))

		return ret_res
		
class PaperTranslator(object):
	'''
	latex translator
	features:
	- preserve citations
	- preserve latex symbols, e.g. \textbf{}
	- preserve equation code

	not included:
	- figure, table or algorithms
	'''
	def __init__(self, fromLang='en', toLang='zh', appid=None, secretKey=None, url=None):
		if not appid or not secretKey:
			raise ValueError('appid and secretKey must be specified')

		self.translator = Translator(appid, secretKey,url, fromLang, toLang)

		self.citation_cache_dict = {}
		self.ref_cache_dict = {}
		self.equation_cache_dict = {}
		self.sym_cache_dict = {}

	def preprocess(self, src_text):
		"""
		The text length after preprocessing should not be larger than 2000.
		basic rules:
		1. math formulation in $$ does not change
		2. \\xx such sign should be replaced
		3. repalce all cite or ref
		"""
		# match all \bf and {} in the text

		cite_patten = r"[~]?\\cite{.*?}"

		ref = r"[~]?\\ref{.*?}"

		equation = r"\$.*?\$"

		sym_patten = r"\\{.*?}\{"

		all_cite = re.findall(cite_patten, src_text, re.S)
		self.citation_cache_dict = {k:v for k,v in enumerate(all_cite)}
		src_text = re.sub(cite_patten, ' **', src_text)


		all_ref = re.findall(ref, src_text, re.S)
		self.ref_cache_dict = {k:v for k,v in enumerate(all_ref)}
		src_text = re.sub(ref, ' *^*', src_text)

		all_eq = re.findall(equation, src_text, re.S)
		
		self.equation_cache_dict = {k:v for k,v in enumerate(all_eq)}
		src_text = re.sub(equation, '*^^*', src_text)
		
		all_sym = re.findall(sym_patten, src_text, re.S)
		self.sym_cache_dict = {k:v for k,v in enumerate(all_sym)}
		src_text = re.sub(sym_patten, '*^^^*', src_text)

		src_text = src_text.replace('{','[').replace('}',']')

		return src_text

	def post_replace(self, patten, mode, text):
		config_dict = {'eq': self.equation_cache_dict, 'ref': self.ref_cache_dict,
						'cite': self.citation_cache_dict, 'sym': self.sym_cache_dict}
		q = text.find(patten)
		# print(q)
		cnt = 0
		while q != -1:
			text = text[:q] + config_dict[mode][cnt] + text[q+len(patten):]
			q = text.find(patten)
			cnt += 1
		return text

	def postprocess(self, tran_text):
		# replace all [] to {}
		tran_text = tran_text.replace('[','{').replace(']','}')
		# tran_text = tran_text.replace('****','').replace('qq','QQ').replace('sss','SSS')
		tran_text = self.post_replace(r'*^^^*', 'sym', tran_text)
		tran_text = self.post_replace(r'*^^*', 'eq', tran_text)
		tran_text = self.post_replace(r'*^*', 'ref', tran_text)
		tran_text = self.post_replace(r'**', 'cite', tran_text)
		return tran_text

	def translate(self, src_text):

		pp_text = self.preprocess(src_text)
		tran_text = self.translator.translate(pp_text)
		res_text = self.postprocess(tran_text)
		return res_text

# if __name__=='__main__':
# 	URL = 'http://api.fanyi.baidu.com' + '/api/trans/vip/translate'
# 	translator = PaperTranslator(appid='20190814000326508',secretKey='Cuqivm6X0cOdvCYOcEm6',url=URL)
# 	#text = "For example, ~\\cite{zhang2018deep}  exploited a two-way knowledge transfer and demonstrated that training two networks simultaneously has a potential performance improvement over conventional distillation. ~\\cite{anil2018large} investigated the "
# 	text = r"From Eq.~(\ref{eq:admm}), we can see that ADMM essentially decouples the functions $h$ and $o$, and makes it possible to exploit the individual structures of $h$ and $o$. Thus, the optimization procedure can be efficient and parallelizable.\
# 			Although the ADMM method was proposed to solve convex problems, many studies have shown that this approach can be used in non-convex cases, such as nonnegative matrix factorization~\cite{boyd2011distributed} and network lasso~\cite{hallac2015network}."
# 	print(translator.preprocess(text))
# 	print(translator.translate(text))

	# tran_text = u'例如，MM利用双向知识转移，证明了同时训练两个网络比传统蒸馏有潜在的性能改进。MM调查了'
	# m = tran_text.find('MM')
	# while m != -1:
	# 	tran_text =  tran_text[:m] + '\\cite{hello}' + tran_text[m+2:]
	# 	m = tran_text.find('MM')
	# print(tran_text)
