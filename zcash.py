import sys
import json
from urllib.request import Request, urlopen, HTTPError
from urllib.parse import urlencode

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
    print(f'Usage:\n{sys.argv[0]} [network|block-by-hash <hash>|block-by-height <height>|anchor-of <txid> <joinsplit-index>|tx <txid>]')
    quit()

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
    case 'anchor-of':
        # given a block height and an anchor, look for that anchor backwards from the given height
        if len(sys.argv) < 4:
            usage()
        chunk_size = 100
        height = sys.argv[2]
        anchor = sys.argv[3]
        for i in range(height, 0, -1):
            getblockio_req({'method': 'getblock', 'params': ''})
    case _:
        resp = getblockio_req({'method': sys.argv[1], 'params': sys.argv[2:]})

print(json.dumps(resp, indent=4))
