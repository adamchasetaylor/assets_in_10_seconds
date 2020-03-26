# assets_in_10_seconds
Creates a short lived asset on Twilio's Serverless Platform for demo purposes

This script reads TWILO_ACCOUNT_SID and TWILIO_AUTH_TOKEN from your environment.

Then the script does the following:

1. Creates a Service using Helper Library
2. Creates an Environment using Helper Library
3. Creates an Asset using Helper Library
4. Creates an Asset Version with Public Visibility using Custom TwilioHttpClient
5. Creates a Build Using Helper Library
6. Waits 10 seconds for Build to Finish
7. Creates a Deployment Using Helper Library
8. Prints the Domain Name and Path of Asset
9. Prints the Twilio SIDs created
10. Waits 10 seconds for you to check out your new asset
11. Deletes the Service using Helper Library
