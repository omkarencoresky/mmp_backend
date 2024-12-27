# myapp/views.py
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.models import User
from requests_oauthlib import OAuth2Session
from common_app.models import OAuthApplication, OAuthAccessToken, OAuthRefreshToken
from datetime import datetime, timedelta

# OAuth2 client credentials
CLIENT_ID = '20f50c50-801b-4974-910f-483658a3cc2e'
CLIENT_SECRET = '9f67ca89-a972-4dd1-b619-55a8923f1ee9'
AUTHORIZATION_URL = 'https://oauth-provider.com/authorize'
TOKEN_URL = 'https://oauth-provider.com/token'
REDIRECT_URI = 'http://localhost:8000/oauth/callback/'

# OAuth Login view
def oauth_login(request):
    print('this is running')
    oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
    authorization_url, state = oauth.authorization_url(AUTHORIZATION_URL)
    return redirect(authorization_url)


# OAuth Callback view to exchange authorization code for tokens
def oauth_callback(request):
    oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
    authorization_response = request.build_absolute_uri()
    
    # Fetch access token using the authorization code
    oauth.fetch_token(TOKEN_URL, authorization_response=authorization_response, client_secret=CLIENT_SECRET)
    
    # Store access token in the database
    access_token = oauth.token['access_token']
    refresh_token = oauth.token['refresh_token']
    expires_in = oauth.token['expires_in']
    
    expiration_time = datetime.now() + timedelta(seconds=expires_in)
    
    # Store in OAuthAccessToken table
    OAuthAccessToken.objects.create(
        user=request.user,  # Assuming the user is already logged in
        token=access_token,
        expires=expiration_time,
        scope="read write",  # Define scopes if needed
        client=OAuthApplication.objects.get(client_id=CLIENT_ID),
        refresh_token=refresh_token
    )
    
    return JsonResponse({'message': 'OAuth login successful', 'access_token': access_token})


# API view to validate the access token
def api_view(request):
    token = request.headers.get('Authorization')
    if not token:
        return JsonResponse({'error': 'Authorization header missing'}, status=400)
    
    try:
        access_token = OAuthAccessToken.objects.get(token=token)
        if access_token.expires < datetime.now():
            return JsonResponse({'error': 'Token expired'}, status=400)
        
        # Continue processing the API view logic...
        return JsonResponse({'message': 'Protected API data'})
    except OAuthAccessToken.DoesNotExist:
        return JsonResponse({'error': 'Invalid token'}, status=400)


# Refresh token view
def refresh_token(request):
    refresh_token = request.POST.get('refresh_token')
    try:
        refresh_token_obj = OAuthRefreshToken.objects.get(token=refresh_token)
        access_token = refresh_token_obj.access_token

        oauth = OAuth2Session(CLIENT_ID, token={'refresh_token': refresh_token})
        new_token = oauth.refresh_token(TOKEN_URL, client_secret=CLIENT_SECRET)

        access_token.token = new_token['access_token']
        access_token.expires = datetime.now() + timedelta(seconds=new_token['expires_in'])
        access_token.save()

        return JsonResponse({'access_token': new_token['access_token']})
    except OAuthRefreshToken.DoesNotExist:
        return JsonResponse({'error': 'Invalid refresh token'}, status=400)
