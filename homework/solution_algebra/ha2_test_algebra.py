import json
import ha2lib_algebra as ha

f = open("../testDBs/sampleUnivDB.json", "r")
input = json.loads(f.read())

output = ha.ha2(input)

print(json.dumps(output))
