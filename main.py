import os
import time
import json
from twilio.rest import Client
from customRequest import MyRequestClass

# To Handle File Paths
from pathlib import Path

# Load ENV Variables
from dotenv import load_dotenv
load_dotenv()

# Load Clients
from twilio.rest import Client

# Your Account Sid and Auth Token from twilio.com/console
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

# Setup Default Twilio Client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Use MyRequestClass to Create Custom Upload Client
upload_auth = (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
upload_http_client = MyRequestClass()

# Create Service
# https://www.twilio.com/docs/runtime/functions-assets-api/api/service#create-a-service-resource

service = client.serverless.services.create(
  include_credentials=True,
  unique_name='my-new-app2',
  friendly_name='My New App'
)

# Create Environment
# https://www.twilio.com/docs/runtime/functions-assets-api/api/environment#create-an-environment-resource

environment = client.serverless \
  .services(service.sid) \
  .environments \
  .create(domain_suffix='stage', unique_name='staging')

# Create Asset

asset = client.serverless \
  .services(service.sid) \
  .assets \
  .create(friendly_name='friendly_name')

# Create Asset Version
# This is using a custom 
# Files hint from https://stackoverflow.com/questions/58278283/how-to-fix-unsupported-media-type-error-on-python-post-request-to-twilio

remote_path = '/myfile.txt'
remote_visibility = 'public'

asset_folder = 'assets'
asset_file = 'myfile.txt'
asset_type = 'text/plain'
asset_path = Path(asset_folder+"/"+asset_file)

url = f"https://serverless-upload.twilio.com/v1/Services/{service.sid}/Assets/{asset.sid}/Versions"
payload = {'Path': remote_path, 'Visibility': remote_visibility}
files = {'Content': (asset_file, open(asset_path, 'rb'), asset_type)}
response = upload_http_client.request('POST', url, data = payload, files = files, auth = upload_auth)

asset_version = json.loads(response.text)
asset_versions = [ asset_version["sid"] ]

# Create a Build

build = client.serverless \
  .services(service.sid) \
  .builds \
  .create(
    asset_versions=asset_versions
  )

# Wait for Build

print("Creating Service")
print("##########")
time.sleep(10)

# Create a Deployment

deployment = client.serverless \
  .services(service.sid) \
  .environments(environment.sid) \
  .deployments \
  .create(
    build_sid=build.sid
  )

# Show URL

print(f"http://{environment.domain_name}{remote_path}")

# Cleanup

print("##########")
print(f"Service Sid: {service.sid}")
print(f"Environment Sid: {environment.sid}")
print(f"Asset Sid: {asset.sid}")
print(f"Asset Version Sid: {asset_version['sid']}")
print(f"Build Sid: {build.sid}")
print(f"Deployment Sid: {deployment.sid}")
print("##########")

# Wait for 1 Minutes to Check
time.sleep(10)

# Delete Service
print("Deleting the Service")
client.serverless.services(service.sid).delete()