from google.cloud import datastore

# Initialize the Datastore client with the correct namespace
client = datastore.Client(project='cloud-varun-varunch', namespace="apiverse")

# Query for API keys
query = client.query(kind='APIKey')
results = list(query.fetch())

if results:
    print("API Keys found in Datastore:")
    for entity in results:
        print(entity)
else:
    print("No API keys found in Datastore.")
