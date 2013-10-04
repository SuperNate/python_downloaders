import requests
import argparse
import os

parser = argparse.ArgumentParser(prog='Mass downloader', description='A simple script that downloads multiple files from URLs specified in a file', add_help=True)
parser.add_argument('-i', '--input', type=str, action='store', help='Used to specify the input file. Otherwise the default urls.txt is used')
parser.add_argument('-d', '--dir', type=str, action='store', help='Specify output directory for downloads')
args=parser.parse_args()

in_file = '/home/sean/urls.txt'
dir = '/home/sean/downloaded'
if args.input == None:
    print 'Using default input file %s' % in_file
else:
    in_file = args.input
        
if args.dir == None:
    print 'Using default output directory %s' % dir
else:
    dir = args.dir
        
if not os.path.exists(dir):
    os.makedirs(dir)

print
f = open(in_file,'rb')
lines = f.readlines()
f.close()
urls = []
for line in lines:
    urls.append(line.strip())

files = [url.split('/')[-1].strip() for url in urls]

for url, file in zip(urls,files):
    print 'Downloading %s' % file
    r = requests.get(url, stream=True)
    out_file = dir + '/' + file
    with open(out_file, 'wb') as f:
        for chunk in r.iter_content(1024):
            f.write(chunk)
                
print 'Finished downloading all files'
