import meilisearch

client = meilisearch.Client('http://localhost:7700', 'myVerySecureKey')

print(client.create_dump())