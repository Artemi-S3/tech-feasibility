# first install meilisearch:
#   curl -L https://install.meilisearch.com | sh
#
# then install the python library
#   pip3 install meilisearch
#
# then launch meilisearch and set a masterkey
#   ./meilisearch --master-key="myVerySecureKey"
#
# you are now free to run the code, make sure not to exit out of meilisearch

import meilisearch
import json

client = meilisearch.Client('http://localhost:7700', 'myVerySecureKey')

jsonFile = open("states.json")
data = json.load(jsonFile)
print(client.index("states").add_documents(data))
