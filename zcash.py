import sys
import json
from urllib.request import Request, urlopen, HTTPError
from urllib.parse import urlencode
from numpy import array_split
from math import ceil

try:
    with open('api-key', 'r') as f:
        api_key = f.read()
except FileNotFoundError:
    print('File "api-key" could not be opened.')
    quit()

url = 'https://zec.getblock.io/'

def getblockio_req(*data):
    header = {
        'x-api-key': api_key.strip(),
        'Content-Type': 'application/json'
    }
    try:
        resp = urlopen(Request(url, json.dumps([datum | {'jsonrpc': '2.0'} for datum in list(data)]).encode('utf-8'),
            header, method='POST'))
    except HTTPError:
        print('getblock.io API returned error.')
        quit()

    return json.loads(resp.read())

def usage():
    print(f'Usage:\n{sys.argv[0]} [<normal RPC>|find-anchor <height> <joinsplit-index>|getblock <start-end>]')
    quit()

def main():
    if len(sys.argv) == 1:
        usage()
    
    match sys.argv[1]:
        case 'getblock':
            verbosity = int(sys.argv[3]) if len(sys.argv) > 3 else 1
            if '-' in sys.argv[2]:
                start,end = list(map(int, sys.argv[2].split('-')))
                resp = getblockio_req()
            else:
                start = int(sys.argv[2])
                end = start
    
            resp = getblockio_req(*[{'method': 'getblock', 'params': [str(i), verbosity]} for i in range(start, end + 1)])
            print(json.dumps(resp, indent=4))
        case 'find-anchor':
            # given a block height and an anchor, look for that anchor backwards from the given height
            if len(sys.argv) < 4:
                usage()
            chunk_size = 1000
            height = int(sys.argv[2])
            anchor = sys.argv[3]
            for subseq in array_split(range(height, 0, -1), ceil(height / chunk_size)):
                blocks = getblockio_req(*[{'method': 'getblock', 'params': [str(j), 1]} for j in subseq])
                print('fetched new chunk')
                for block in blocks:
                    print(f'anchor={block["result"]["blockcommitments"]}')
                    if block['result']['blockcommitments'] == anchor:
                        print('Found.')
                        break
                else:
                    continue
                break
        case _:
            resp = getblockio_req({'method': sys.argv[1], 'params': sys.argv[2:]})
            print(json.dumps(resp, indent=4))

try:
    main()
except KeyboardInterrupt:
    print('KeyboardInterrupt happened.')
    pass
