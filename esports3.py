import requests
import os
import concurrent.futures
import subprocess

page = 'https://directes-tv-es.ccma.cat/live-origin/esport3-hls/0/br3/220712125302/92198/geo-br3_27659'
file_list = []
ts_file_list = []
os.makedirs('downloads', exist_ok = True)

def threaded_downloads(page, index):
	request = requests.get(page + str(index) + '.ts', stream=True).content
	with open('downloads/'+str(index)+'.ts','wb') as ts:
		ts.write(request)
		
with concurrent.futures.ThreadPoolExecutor(80) as executor:
	for i in range(1400,2000):
		executor.submit(threaded_downloads, page, i)

for file_ in os.listdir('downloads'):
	file_list.append(file_)

ts_file_list = sorted(file_list)


with open('ts_file_list','a') as file_list:
	for ts_file in ts_file_list:
		file_list.write('file downloads/'+ts_file+'\n')
file_list.close()

file_name = input('Enter output file name: ')
command = ['ffmpeg','-f','concat','-safe','0','-i','ts_file_list','-c','copy',str(file_name)+'.avi']
subprocess.run(command, shell = False) 
	
		
