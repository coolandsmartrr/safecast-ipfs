import urllib, json, datetime, csv, pandas, ipfsapi
import os
import subprocess

## RETRIEVE DAILY DATA

# Set Retrieve Date
today = datetime.datetime.today()
captured_after = today

# Set request URL
api_url = "https://api.safecast.org/measurements.json"
request_url = api_url + "?captured_after=" + captured_after.strftime("%Y-%m-%d+00%3A00")

# DEBUG:
print request_url

# Retrieve data
response = urllib.urlopen(request_url)
data = json.loads(response.read())
print data

# Set filename as today's date
filename = today.strftime("%Y%m%d-%H%M%S")

# Save json into file
with open(filename + '.json', 'w') as outfile:
    json.dump(data, outfile)

# Save json into csv
df = pandas.read_json(filename + ".json")
print(df)
df.to_csv(filename + ".csv", mode="a", header=False)

## UPLOAD CSV onto IPFS

# Start ipfs daemon
cmd = "ipfs daemon &"
pid = os.fork()
if pid == 0:
  os.system("nohup ipfs daemon &")
  exit()

# Upload csv
api = ipfsapi.connect('127.0.0.1', 5001)
res = api.add(filename + ".csv")
print res


## TIMESTAMP

# Upload csv to timestamp server
""" ots has to be installed """
subprocess.call("ots stamp " + filename + ".csv", shell=True)