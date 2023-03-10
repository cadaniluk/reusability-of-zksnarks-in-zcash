import sys
import json
from urllib.request import Request, urlopen, HTTPError

url_base = 'https://api.zcha.in/v2/mainnet/'

def zchain_req(url):
    header = {
        'User-Agent': 'must specify otherwise zcha.in refuses'
    }
    try:
        resp = urlopen(Request(url, None, header))
    except HTTPError:
        print('zcha.in API returned error.')
        quit()

    return json.loads(resp.read())

def get_tx(txid):
    return zchain_req(url_base + f'transactions/{txid}')


def usage():
    print(f'Usage:\n{sys.argv[0]} [network|block-by-hash <hash>|block-by-height <height>|anchor-of <txid> <joinsplit-index>|tx <txid>]')
    quit()

if len(sys.argv) == 1:
    usage()

match sys.argv[1]:
    case 'network':
        url_ext = 'network'
    case 'block-by-hash':
        if len(sys.argv) < 3:
            usage()
        url_ext = f'blocks/{sys.argv[2]}'
    case 'block-by-height':
        if len(sys.argv) < 3:
            usage()
        url_ext = f'blocks?sort=height&direction=ascending&limit=1&offset={int(sys.argv[2]) - 1}'
    case 'anchor-of':
        if len(sys.argv) < 4:
            usage()
        chunk_size = 100
        anchor = get_tx(sys.argv[2])['vjoinsplit'][int(sys.argv[3])]['anchor']
    case 'tx':
        if len(sys.argv) < 3:
            usage()
        print(json.dumps(get_tx(sys.argv[2]), indent=4))
        quit()
    case _:
        print(f'Unknown command {sys.argv[1]}.')
        usage()

print(json.dumps(zchain_req(url_base + url_ext), indent=4))
