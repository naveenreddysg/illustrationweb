# -*- coding: utf-8 -*-

import os, sys
import flask
import requests
from dateutil.relativedelta import relativedelta
from datetime import timedelta, datetime as day
from get_data import mainClass
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from utilities import (
    get_dates, get12months, change, get_two_month_dates, prev_month_last_year,  last_year, credentials_to_dict
)
from ResultServices.results import SessionsCategoryResults, WebsiteTrafficResults, BounceRateResults, AvgSessionDuration,Conversions


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
  present = mainClass(sys.argv, dates[0]['pre_start'], dates[0]['pre_end'], service)
  previous = mainClass(sys.argv, dates[0]['prv_start'], dates[0]['prv_end'], service)
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
  AllVisitors_pre, AllVisitors_prev, MobileTablet_pre, MobileTablet_prev, Return_pre, Return_prev = [], [], [], [], [], []
  for item1, item2 in zip(result['traffic']['AllTraffic']['present'][0:30],
                          result['traffic']['AllTraffic']['previous'][0:30]):
      AllVisitors_pre.append(item1["All Traffic"])
      AllVisitors_prev.append(item2["All Traffic"])
  for item3, item4 in zip(result['traffic']['MobileTabletTraffic']['present'][0:30],
                          result['traffic']['MobileTabletTraffic']['previous'][0:30]):
      MobileTablet_pre.append(item3['traffic'])
      MobileTablet_prev.append(item4['traffic'])
  for item5, item6 in zip(result['traffic']['returningusers']['present'][0:30],
                          result['traffic']['returningusers']['previous'][0:30]):
      Return_pre.append(item5['traffic'])
      Return_prev.append(item6['traffic'])
  visitors = {'visits': sum(AllVisitors_pre), 'change_visits': round(
      ((float(sum(AllVisitors_pre)) - float(sum(AllVisitors_prev))) / float(sum(AllVisitors_prev))) * 100, 2),
              'MobileTablet_visits': sum(MobileTablet_pre), 'change_MobileTablet_visits': round(
          ((float(sum(MobileTablet_pre)) - float(sum(MobileTablet_prev))) / float(sum(MobileTablet_prev))) * 100, 2),
              'Return_visits': sum(Return_pre), 'change_Return_visits': round(
          ((float(sum(Return_pre)) - float(sum(Return_prev))) / float(sum(Return_prev))) * 100, 2)
              }

  dates = {
      'pre_date': dates[1]['pre_start'] + ' to ' + dates[1]['pre_end'],
      'prev_date': dates[1]['prv_start'] + ' to ' + dates[1]['prv_end']
  }

  keys = (sessions['sessions']['present'][0].keys())
  keys = [x for x in keys if x != 'Country']
  Change = {
      i: change(source=i, result=sessions['sessions']) for i in keys
  }
  days = [((day.now() - timedelta(days=i)).strftime("%A")) for i in range(1, 8)]

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


if __name__ == '__main__':

  # When running locally, disable OAuthlib's HTTPs verification.
  # ACTION ITEM for developers:
  #     When running in production *do not* leave this option enabled.

  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

  # Specify a hostname and port that are set as a valid redirect URI

  # for your API project in the Google API Console.

  port = int(os.environ.get("PORT", 8080))
  app.run(host="localhost", debug=True, port=port)