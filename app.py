# -*- coding: utf-8 -*-

import os
import flask
import requests

from get_data import mainClass
from ResultServices.results import SessionsCategoryResults, WebsiteTrafficResults, BounceRateResults, AvgSessionDuration,Conversions
from utilities import (
    get_dates, get12months, change, get_two_month_dates, prev_month_last_year,  last_year, credentials_to_dict
)

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
API_SERVICE_NAME = 'analytics'
API_VERSION = 'v3'


app = flask.Flask(__name__)

# Note: A secret key is included in the sample so that it works.
# If you use this code in your application, replace this with a truly secret
# key. See http://flask.pocoo.org/docs/0.12/quickstart/#sessions.
app.secret_key = 'sdvnkcklasdhuv.bfvlduvhldfbvbfkvmfnbv'


@app.route('/')
def index():
  if 'credentials' not in flask.session:
    return flask.redirect('authorize')

  credentials = google.oauth2.credentials.Credentials(
      **flask.session['credentials'])

  service = googleapiclient.discovery.build(
      API_SERVICE_NAME, API_VERSION, credentials=credentials)

  option = 'Last 7 days'
  dates = get_dates(7)
  present = mainClass(dates[0]['pre_start'], dates[0]['pre_end'], service)
  previous = mainClass(dates[0]['prv_start'], dates[0]['prv_end'], service)
  sessions = SessionsCategoryResults(present, previous, 'date').main()
  conversions = Conversions(present, previous, 'month').main()
  traffic = WebsiteTrafficResults(present, previous, 'date').main()
  bouncerate = BounceRateResults(present, previous).main()
  avgduration = AvgSessionDuration(present, previous).main()
  result = {
      "sessions": sessions['totalSessions'],
      "session_category": sessions['sessions']['present'],
      'traffic': traffic,
      'conversions': conversions,
      'session_category_line_data': sessions['session_category_line_data'],
      'session_region_line_data': sessions['session_region_line_data'],
      'bouncerate': bouncerate,
      'avgduration': avgduration,
  }

  flask.session['credentials'] = credentials_to_dict(credentials)

  return flask.render_template("result.html", result=result)


@app.route('/authorize')
def authorize():
  # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES)

  flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

  authorization_url, state = flow.authorization_url(
      # Enable offline access so that you can refresh an access token without
      # re-prompting the user for permission. Recommended for web server apps.
      access_type='offline',
      # Enable incremental authorization. Recommended as a best practice.
      include_granted_scopes='true')

  # Store the state so the callback can verify the auth server response.
  flask.session['state'] = state

  return flask.redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
  # Specify the state when creating the flow in the callback so that it can
  # verified in the authorization server response.
  state = flask.session['state']

  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
  flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

  # Use the authorization server's response to fetch the OAuth 2.0 tokens.
  authorization_response = flask.request.url
  flow.fetch_token(authorization_response=authorization_response)

  # Store credentials in the session.
  # ACTION ITEM: In a production app, you likely want to save these
  #              credentials in a persistent database instead.
  credentials = flow.credentials
  flask.session['credentials'] = credentials_to_dict(credentials)

  return flask.redirect(flask.url_for('index'))


@app.route('/revoke')
def revoke():
  if 'credentials' not in flask.session:
    return ('You need to <a href="/authorize">authorize</a> before ' +
            'testing the code to revoke credentials.')

  credentials = google.oauth2.credentials.Credentials(
    **flask.session['credentials'])

  revoke = requests.post('https://accounts.google.com/o/oauth2/revoke',
      params={'token': credentials.token},
      headers = {'content-type': 'application/x-www-form-urlencoded'})

  status_code = getattr(revoke, 'status_code')

  if status_code == 200:

    return flask.jsonify({"status": 'Success'})


def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}


if __name__ == '__main__':

  # When running locally, disable OAuthlib's HTTPs verification.
  # ACTION ITEM for developers:
  #     When running in production *do not* leave this option enabled.

  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

  # Specify a hostname and port that are set as a valid redirect URI

  # for your API project in the Google API Console.

  port = int(os.environ.get("PORT", 8080))
  app.run(host="localhost", debug=True, port=port)