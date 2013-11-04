import requests
import argparse
import os

parser = argparse.ArgumentParser(prog='Download Accelerator', description='Downloads a single file from a URL in parallel', add_help=True)
# parser.add_argument('-u', '--url', type=str, action='store', help='The URL of the file to be downloaded')
parser.add_argument('-n', '--num', type=int, action='store', help='The number of threads to be used to download the file', default=1)
parser.add_argument('url', type=str, help='The URL of the file to be downloaded')
args=parser.parse_args()

file_name = 'index.html'
args.url = args.url.strip()

if args.url[-1] != '/':
    file_name = args.url.split('/')[-1].strip()

if args.url[0:7] != 'http://':
    args.url = 'http://' + args.url

head = requests.head(args.url)
length = int(head.headers['content-length'])

import sys
if length < 0:
    print 'Not a valid content-length'
    sys.exit(1)

chunk_size = length / args.num
chunks = []
chunks.append(0)
temp = 0

# create proper ranges for downloading from within each thread
i = 0
while i < args.num:
    temp += chunk_size
    if temp >= length or i == (args.num - 1):
        temp = length
    chunks.append(temp)
    i += 1

import threading
class myThread(threading.Thread):
    def __init__(self, url, range_string):
        threading.Thread.__init__(self)
        self.url = url
        self.range_string = range_string
        self.r = None
    def run(self):
        r = requests.get(self.url, headers={'Range':self.range_string})
        self.r = r

threads = []
i = 0
j = 1
import time
start = time.time()
while i < args.num:
    if i == 0:
        range_str = 'bytes=%d-%d' % (0, chunks[j])
    else:
        range_str = 'bytes=%d-%d' % (chunks[j-1]+1, chunks[j])
    thread = myThread(args.url, range_str)
    threads.append(thread)
    i += 1
    j += 1
                
for t in threads:
    t.start()

f = open(file_name,'wb')

for t in threads:
    t.join()
    for chunk in t.r.iter_content(10000):
        f.write(chunk)

total_time = time.time() - start
f.close()

print '%s %d %d %f' % (args.url.strip(), args.num, length, total_time)
