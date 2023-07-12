import sys
import json
from urllib.request import Request, urlopen, HTTPError
from urllib.parse import urlencode
from numpy import array_split
from math import ceil

def chunks(end, start=0, verbosity=1):
    chunk_size = 100
    for subseq in array_split(range(end, start - 1, -1), ceil((end - (start - 1)) / chunk_size)):
        yield getblockio_req(*[{'method': 'getblock', 'params': [str(j), verbosity]} for j in subseq])

def parse_range(range_str):
    if '-' in sys.argv[2]:
        start, end = list(map(int, range_str.split('-')))
    else:
        start = int(sys.argv[2])
        end = start
    return start, end

def getblockio_req(*data):
    url = 'https://zec.getblock.io/'
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
    print(f'Usage:\n{sys.argv[0]} [<normal RPC>|find-anchor <height> <anchor>|getblock <start-end>]|find-joinsplit <start-end>|find-spend-or-output <start-end>|find-action <start-end>|show-tx <txid>')
    quit()

def main():
    global api_key

    if len(sys.argv) == 1:
        usage()

    try:
        with open('api-key', 'r') as f:
            api_key = f.read()
    except FileNotFoundError:
        print('File "api-key" could not be opened.')
        quit()
    
    match sys.argv[1]:
        case 'getblock':
            verbosity = int(sys.argv[3]) if len(sys.argv) > 3 else 1
            start, end = parse_range(sys.argv[2])
            resp = getblockio_req(*[{'method': 'getblock', 'params': [str(i), verbosity]} for i in range(start, end + 1)])
            print(json.dumps(resp, indent=4))
        case 'find-anchor':
            # given a block height and an anchor, look for that anchor backwards from the given height
            if len(sys.argv) < 4:
                usage()
            height = int(sys.argv[2])
            anchor = sys.argv[3]
            for blocks in chunks(height):
                print(f'Searching {blocks[-1]["result"]["height"]}-{blocks[0]["result"]["height"]}...')
                for block in blocks:
                    print(f'block {block["result"]["height"]}: anchor={block["result"]["anchor"]}')
                    if block['result']['anchor'] == anchor or block['result']['blockcommitments'] == anchor:
                        print(f'Found anchor in block {block["result"]["height"]}.')
                        break
                else:
                    continue
                break
        case 'find-joinsplit':
            end, start = parse_range(sys.argv[2])
            for blocks in chunks(end, start, verbosity=2):
                print(f'Searching {blocks[-1]["result"]["height"]}-{blocks[0]["result"]["height"]}...')
                for block in blocks:
                    for tx in block['result']['tx']:
                        if tx.get('vjoinsplit', []) != []:
                            print(f'Found shielded transaction in block {block["result"]["height"]}, TX {tx["txid"]}.')
                            break
                    else:
                        continue
                    break
                else:
                    continue
                break
        case 'find-spend-or-output':
            end, start = parse_range(sys.argv[2])
            for blocks in chunks(end, start, verbosity=2):
                print(f'Searching {blocks[-1]["result"]["height"]}-{blocks[0]["result"]["height"]}...')
                for block in blocks:
                    for tx in block['result']['tx']:
                        if tx.get('vShieldedSpend', []) != [] or tx.get('vShieldedOutput', []) != []:
                            print(f'Found shielded transaction in block {block["result"]["height"]}, TX {tx["txid"]}.')
                            break
                    else:
                        continue
                    break
                else:
                    continue
                break
        case 'find-action':
            end, start = parse_range(sys.argv[2])
            for blocks in chunks(end, start, verbosity=2):
                print(f'Searching {blocks[-1]["result"]["height"]}-{blocks[0]["result"]["height"]}...')
                for block in blocks:
                    for tx in block['result']['tx']:
                        if tx.get('orchard', []) != []:
                            print(f'Found shielded transaction in block {block["result"]["height"]}, TX {tx["txid"]}.')
                            break
                    else:
                        continue
                    break
                else:
                    continue
                break
        case 'show-tx':
            raw_tx = getblockio_req({'method': 'getrawtransaction', 'params': [sys.argv[2]]})
            tx = getblockio_req({'method': 'decoderawtransaction', 'params': [raw_tx[0]['result']]})
            print(json.dumps(tx, indent=4))
        case _:
            resp = getblockio_req({'method': sys.argv[1], 'params': sys.argv[2:]})
            print(json.dumps(resp, indent=4))

try:
    main()
except KeyboardInterrupt:
    print('KeyboardInterrupt happened.')
    pass
