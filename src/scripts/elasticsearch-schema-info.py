import json
from typing import List
from git_root import git_root

def main():
    filename = git_root('jsonld/trait-value.jsonld')

    with open(filename) as f:
        jsonld  = json.load(f)

    slots:List = jsonld['slots']
    for slot in slots:
        # print(slot.keys(), slot.values())
        for k,v in slot.items():
            print(k, v)
        

if __name__ == "__main__":
    main()