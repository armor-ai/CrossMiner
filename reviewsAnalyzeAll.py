#!/usr/bin/env python
#-*- coding: utf-8 -*-
# __author__ = "Yichuan Man"
# __version__ = "1.0"
# __date__ = "29/4/2016"

import os
import re
import sys
import math
import json
import yaml
import gensim
import numpy as np
from sklearn.cluster import KMeans
from os import listdir
from os.path import isfile, join

class InputFile(object):
	def __init__(self):
		pass

	def get_folder_names(self, path):
		return [x for x in os.walk(path).next()][1]

	def get_file_names(self, path, suffix):
		files = [f for f in listdir(path) if isfile(join(path, f))]
		return [f for f in files if f.endswith(suffix)]

	def get_file_data(self, path, name, split_symbol, pos):
		data = read_data(path, name, split_symbol, pos)
		return data

class DataAnalyze(object):
	def __init__(self):
		pass

	def get_all_apps_info(self):
		pass

def read_data(path, name, split_symbol, pos):
	file = open(os.path.join('', path, name))
	data = list()
	for idx, line in enumerate(file):
		line = line.split(split_symbol)[pos]
		data.append(line)
	file.close()
	return data

def save_data(path, name, data):
	if not os.path.exists(path):
		os.makedirs(path)
	name = path + name
	file = open(name, 'w')
	for items in data:
		try:
			text = '******'.join(items)
		except UnicodeDecodeError as e:
			for i in range(len(items)):
				items[i] = re.sub(r'[^\x00-\x7F]+', ' ', items[i])
			text = '******'.join(items)
		try:
			file.write(u''.join((text, "\n")).encode("utf-8"))
		except UnicodeDecodeError as e:
			text = re.sub(r'[^\x00-\x7F]+', ' ', text)
			file.write(u''.join((text, "\n")).encode("utf-8"))
	file.close()

if __name__ == '__main__':
	inputFile   = InputFile()
	apps_num    = 20
	similar_num = 20
	# suffix_list  = ['_clusters_dic_all.txt', '_clusters_dic_after.txt']
	suffix_list   = ['_clusters_dic_after.txt']
	topic_list    = ['battery', 'connection', 'crash', 'memory', 'privacy', 'spam', 'ui']
	platform_list = ['Specific_apps_google', 'Specific_apps_iTunes', 'Specific_apps_microsoft']
	remove_list   = [['cpu', 'ram', 'memory', 'foreground'], [], [], [], [], [], []]

	# getting all apps in different platforms
	print '\ngetting all apps in different platforms...'
	apps_list = [[] for i in range(len(platform_list))]
	for idx, platform in enumerate(platform_list):
		path = 'Output/' + platform
		folders = inputFile.get_folder_names(path)
		for i in range(len(folders)):
			# if len(apps_list) == apps_num:
			apps_list[idx].append(folders[i])
			# else:
				# apps_list.append([folders[i]])

	print("app_list is ", apps_list)
				
	for topic in topic_list:
		topic_no = topic_list.index(topic)
		print '\nTopic: %s starting...' % topic
		for suffix in suffix_list:
			print '\nSuffix: %s starting...' % suffix
			print '\ngetting similar words...'
			topic_words  = dict()
			summary_data = list()
			for platform in platform_list:
				model_path    = 'Output/Skip_gram_results/All_apps'
				model         = gensim.models.KeyedVectors.load_word2vec_format(os.path.join('', model_path, 'All_apps_dl.txt'))
				origi_words   = model.most_similar(topic, topn=similar_num)
				origi_words   = [word[0] for word in origi_words]
				origi_words.insert(0, topic)
				cluster_path  = 'Output/Skip_gram_results/All_apps'
				cluster_name  = 'All_apps' + suffix
				cluster_words = yaml.load(open(os.path.join('', cluster_path, cluster_name)).readline())
				cluster_no    = cluster_words[topic]
				removed_words = list()
				final_words   = list()
				for word in origi_words:
					if word not in cluster_words:
						removed_words.append(word)
						continue
					# if cluster_words[word] != cluster_no:
					# 	removed_words.append(word)
					# 	continue
					if word in remove_list[topic_no]:
						removed_words.append(word)
						continue
					final_words.append(word)
				# final_words = final_words[:10]
				topic_words[platform]= [origi_words, removed_words, final_words]
				summary_data.extend([[platform + '_origi_words: ' + ' '.join(origi_words)], [platform + '_remove_words: ' + ' '.join(removed_words)], 
									[platform + '_final_words: ' + ' '.join(final_words)]])

			raw_review_num        = [0, 0, 0]
			raw_review_rating     = [0, 0, 0]
			clean_review_num      = [0, 0, 0]
			clean_review_rating   = [0, 0, 0]
			keyword_review_num    = [0, 0, 0]
			keyword_review_rating = [0, 0, 0]
			low_review_num        = [0, 0, 0]
			low_review_rating     = [0, 0, 0]

			for platform_num, apps in enumerate(apps_list):
				app_name = apps[0].split('_')[0]
				analyze_data = [[], [], [], [], [], 
								[], [], [], [], [],
								[], [], [], [], []]
				analyze_data[0] = app_name
				for app_no in range(len(apps)):
					app        = apps[app_no]
					print '\nAPP: %s starting...' % app 
					platform   = platform_list[platform_num]

					# getting raw data info
					path   = 'Input/' + platform
					name   = app + '_raw_data.txt'
					data   = read_data(path, name, '\n', 0)
					raw_num    = 0
					raw_rating = 0
					for line in data:
						line = line.split('******')
						if line[5] == 'None':
							continue
						raw_num    += 1
						raw_rating += float(line[5])
					raw_review_num[app_no]    += raw_num
					raw_review_rating[app_no] += raw_rating
					# if num:
					# 	rating = round(rating / num, 5)

					# getting clean data info
					path   = 'Output/' + platform + '/' + app
					name   = app + '_clean_data.txt'
					data   = read_data(path, name, '\n', 0)
					clean_num    = 0
					clean_rating = 0
					for line in data:
						line = line.split('******')
						if line[5] == 'None':
							continue
						clean_num    += 1
						clean_rating += float(line[5])
					clean_review_num[app_no]    += clean_num
					clean_review_rating[app_no] += clean_rating
					# if num:
					# 	rating = round(rating / num, 5)

					# getting clean data
					words        = topic_words[platform][2]
					path         = 'Output/' + platform + '/' + app
					name         = app + '_clean_data.txt'
					clean_data   = read_data(path, name, '\n', 0)
					keywords_num = 0
					keywords_rating = 0
					clean_low_num    = 0
					clean_low_rating = 0
					for line in clean_data:
						line = line.split('******')
						if line[5] == 'None':
							continue
						clean_review = line[2].split()
						if topic in clean_review:
							keywords_num    += 1
							keywords_rating += float(line[5])
							if float(line[5]) <= 2.0:
								clean_low_num    += 1
								clean_low_rating += float(line[5])
							continue

						sentences = list()
						start = 0
						end   = 0
						for i in range(len(clean_review)):
							if not re.match(r"^[a-zA-Z0-9_',]*$", clean_review[i]):
								sentence = [word for word in clean_review[start:end] if word != ',']
								if sentence:
									sentences.append(sentence)
								start = i + 1
							end = i + 1
							if end == len(clean_review):
								sentence = [word for word in clean_review[start:end] if word != ',']
								if sentence:
									sentences.append(sentence)
						for sentence in sentences:
							simi_words = 0
							flag       = False
							for word in words[1:]:
								if word in sentence:
									simi_words += 1
									if simi_words >= 2:
										keywords_num    += 1
										keywords_rating += float(line[5])
										if float(line[5]) <= 2.0:
											clean_low_num    += 1
											clean_low_rating += float(line[5])	
										flag = True
										break
							if flag:
								break
					keyword_review_num[app_no]    += keywords_num
					keyword_review_rating[app_no] += keywords_rating
					low_review_num[app_no]        += clean_low_num
					low_review_rating[app_no]     += clean_low_rating

					analyze_data[1].append(str(raw_num))
					analyze_data[2].append(str(clean_num))
					analyze_data[3].append(str(round(float(clean_num) / raw_num, 5)))
					analyze_data[4].append(str(keywords_num))
					analyze_data[5].append(str(round(float(keywords_num) / clean_num, 5)))
					analyze_data[6].append(str(clean_low_num))
					analyze_data[7].append(str(round(float(clean_low_num) / clean_num, 5)))
					if keywords_num:
						analyze_data[8].append(str(round(float(clean_low_num) / keywords_num, 5)))
					else:
						analyze_data[8].append(str(0))

					avr_clean_rating = 0
					if clean_num:
						avr_clean_rating = round(float(clean_rating) / clean_num, 5)
						analyze_data[9].append(str(avr_clean_rating))
					else:
						analyze_data[9].append(str(0))

					avr_keywords_rating = 0
					if keywords_num:
						avr_keywords_rating = round(float(keywords_rating) / keywords_num, 5)
						analyze_data[10].append(str(avr_keywords_rating))
					else:
						analyze_data[10].append(str(0))

					if avr_clean_rating and avr_keywords_rating:
						analyze_data[11].append(str(round((avr_clean_rating - avr_keywords_rating) / avr_clean_rating, 5)))
					else:
						analyze_data[11].append(str(0))

					avr_low_review_rating = 0
					if clean_low_num:
						avr_low_review_rating = round(float(clean_low_rating) / clean_low_num, 5)
						analyze_data[12].append(str(avr_low_review_rating))
					else:
						analyze_data[12].append(str(0))

					if avr_clean_rating and avr_low_review_rating:
						analyze_data[13].append(str(round((avr_clean_rating - avr_low_review_rating) / avr_clean_rating, 5)))
					else:
						analyze_data[13].append(str(0))

					if avr_keywords_rating and avr_low_review_rating:
						analyze_data[14].append(str(round((avr_keywords_rating - avr_low_review_rating) / avr_keywords_rating, 5)))
					else:
						analyze_data[14].append(str(0))

				for i in range(1, len(analyze_data)):
					analyze_data[i] = ' '.join(analyze_data[i])
				# print analyze_data
				summary_data.extend([analyze_data])
				print '\nAPP: %s finished.' % app_name

			all_percent_1 = [0, 0, 0]
			all_percent_2 = [0, 0, 0]
			all_percent_3 = [0, 0, 0]
			all_percent_4 = [0, 0, 0]
			all_percent_5 = [0, 0, 0]
			all_percent_6 = [0, 0, 0]
			all_percent_7 = [0, 0, 0]
			all_percent_8 = [0, 0, 0]
			all_percent_9 = [0, 0, 0]
			all_percent_10 = [0, 0, 0]

			for i in range(3):
				all_percent_1[i] = str(round(float(clean_review_num[i]) / (raw_review_num[i]+1), 5))
				all_percent_2[i] = str(round(float(keyword_review_num[i]) / (clean_review_num[i]+1), 5))
				all_percent_3[i] = str(round(float(low_review_num[i]) / (clean_review_num[i]+1), 5))
				all_percent_4[i] = str(round(float(low_review_num[i]) / (keyword_review_num[i]+1), 5))

				avr_clean_review_rating = 0
				if clean_review_num[i]:
					avr_clean_review_rating = round(float(clean_review_rating[i]) / clean_review_num[i], 5)
					all_percent_5[i] = str(avr_clean_review_rating)
				else:
					all_percent_5[i] = str(0)

				avr_keywords_rating = 0
				if keyword_review_num[i]:
					avr_keywords_rating = round(float(keyword_review_rating[i]) / keyword_review_num[i], 5)
					all_percent_6[i] = str(avr_keywords_rating)
				else:
					all_percent_6[i] = str(0)

				if avr_clean_review_rating and avr_keywords_rating:
					all_percent_7[i] = str(round((float(avr_clean_review_rating) - avr_keywords_rating) / avr_clean_review_rating, 5))
				else:
					all_percent_7[i] = str(0)

				avr_low_review_rating = 0
				if low_review_num[i]:
					avr_low_review_rating = round(float(low_review_rating[i]) / low_review_num[i], 5)
					all_percent_8[i]      = str(avr_low_review_rating)
				else:
					all_percent_8[i] = str(0)

				if avr_clean_review_rating and avr_low_review_rating:
					all_percent_9[i] = str(round((float(avr_clean_review_rating) - avr_low_review_rating) / avr_clean_review_rating, 5))
				else:
					all_percent_9[i] = str(0)

				if avr_keywords_rating and avr_low_review_rating:
					all_percent_10[i] = str(round((float(avr_keywords_rating) - avr_low_review_rating) / avr_keywords_rating, 5))
				else:
					all_percent_10[i] = str(0)

				raw_review_num[i]     = str(raw_review_num[i])
				clean_review_num[i]   = str(clean_review_num[i])
				keyword_review_num[i] = str(keyword_review_num[i])
				low_review_num[i]     = str(low_review_num[i])


			all_data_lis = [' '.join(raw_review_num), ' '.join(clean_review_num), ' '.join(all_percent_1), ' '.join(keyword_review_num),
							' '.join(all_percent_2), ' '.join(low_review_num), ' '.join(all_percent_3), ' '.join(all_percent_4), 
							' '.join(all_percent_5), ' '.join(all_percent_6), ' '.join(all_percent_7), ' '.join(all_percent_8), 
							' '.join(all_percent_9), ' '.join(all_percent_10)]
			summary_data.insert(0, all_data_lis)

			path = 'Output/Analyze_results/All_apps/'
			name = topic + suffix
			save_data(path, name, summary_data)
			print '\nSuffix: %s finished.' % suffix
		print '\nTopic: %s finished.' % topic
	print '\nAll data finished! Well done!'
