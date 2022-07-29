from json import loads

with open("./data/_txtData.json", "r") as f:
    string = f.read()
    print(string[764452: 764472])