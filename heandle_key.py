import os,sys
def get_secret_and_token():
    # get channel_secret and channel_access_token from your environment variable
    channel_secret = os.getenv('LINE_BOT_SECRET_KEY', None)
    channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
    openai_api_key = os.getenv("OPENAI_API_KEY", None)
    if channel_secret is None:
        print('Specify LINE_BOT_SECRET_KEY as environment variable.')
        sys.exit(1)
    if channel_access_token is None:
        print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
        sys.exit(1)

    if openai_api_key is None:
        print('Specify OPENAI_API_KEY as environment variable.')
        sys.exit(1)    
    return {
        'LINE_BOT_SECRET_KEY' : channel_secret,
        'LINE_CHANNEL_ACCESS_TOKEN' : channel_access_token,
        'OPENAI_API_KEY': openai_api_key
    }
