import json


def parse_coordinates():
    resp = []
    filename = 'ride-simple.json'
    data = None
    
    with open(filename, 'r') as f:
        data = json.load(f)

    if data:
        coords = data['features'][0]['geometry']['coordinates']
        resp = coords[:10]

    return resp


def main():
    print(parse_coordinates())
    print(len(parse_coordinates()))


if __name__ == '__main__':
    main()
