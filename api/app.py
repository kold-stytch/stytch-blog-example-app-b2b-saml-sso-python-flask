import os
import sys

from flask import Flask, request, session
from flask_cors import CORS
from stytch import B2BClient

from stytch.b2b.models.organizations import SearchQuery, SearchQueryOperator

import requests
import dotenv

# load the .env file
dotenv.load_dotenv()

# By default, run on localhost:3000
HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", "3000"))

# Load the Stytch credentials, but quit if they aren't defined
STYTCH_PROJECT_ID = os.getenv("STYTCH_PROJECT_ID")
STYTCH_SECRET = os.getenv("STYTCH_SECRET")
if STYTCH_PROJECT_ID is None:
    sys.exit("STYTCH_PROJECT_ID env variable must be set before running")
if STYTCH_SECRET is None:
    sys.exit("STYTCH_SECRET env variable must be set before running")

# NOTE: Set environment to "live" if you want to hit the live api
stytch_client = B2BClient(
    project_id=STYTCH_PROJECT_ID,
    secret=STYTCH_SECRET,
    environment="test",
)

app = Flask(__name__)
CORS(app, supports_credentials=True)  # This will enable CORS for all routes


@app.route("/authenticate", methods=["GET"])
def authenticate():
    token_type = request.args["stytch_token_type"]
    if token_type == "sso":
        resp = stytch_client.sso.authenticate(sso_token=request.arg["token"])
        if resp.status_code != 200:
            return "something went wrong authenticating token"
    else:
        # handle other authentication method callbacks
        return "unsupported auth method"

    # member is successfully logged in
    member = resp.member
    session["stytch_session"] = resp.session_jwt
    return member.json()


@app.route("/org/<string:slug>", methods=["GET"])
def org_index(slug: str):
    resp = stytch_client.organizations.search(
        query=SearchQuery(
            operator=SearchQueryOperator.AND,
            operands=[{"filter_name": "organization_slugs", "filter_value": [slug]}],
        )
    )
    if resp.status_code != 200 or len(resp.organizations) == 0:
        return "Error fetching org"

    organization = resp.organizations[0]
    return organization.json()

    # return render_template(
    #         'organizationLogin.html',
    #         public_token=STYTCH_PUBLIC_TOKEN,
    #         org_name=organization.organization_name,
    #         sso_connections=organization.sso_active_connections
    # )


# run's the app on the provided host & port
if __name__ == "__main__":
    # in production you would want to make sure to disable debugging
    app.run(host=HOST, port=PORT, debug=True)

# @app.route("/authenticate", methods=["POST"])
# def authenticate():
#     token = request.json.get("token")
#     tokenType = request.json.get("type")
#     try:
#         # if tokenType == "sso":
#         resp = client.sso.authenticate(sso_token=token)
#         return handle_authenticate_response(resp), 200
#     # else:
#     #     resp = client.magic_links.authenticate(magic_links_token=token)
#     #     return handle_authenticate_response(resp), 200
#     except Exception as e:
#         return jsonify(error=str(e)), 500

# def handle_authenticate_response(resp):
#     # Basic info
#     status_code = resp.status_code
#     request_id = resp.request_id
#     # Member info
#     member_info = {
#         "member_id": resp.member.member_id,
#         "email_address": resp.member.email_address,
#         "status": resp.member.status,
#         "name": resp.member.name,
#         "is_admin": resp.member.is_admin,
#     }

#     # Session info
#     session_token = resp.session_token
#     session_jwt = resp.session_jwt

#     # Organization info
#     organization_info = {
#         "organization_id": resp.organization.organization_id,
#         "organization_name": resp.organization.organization_name,
#         "organization_slug": resp.organization.organization_slug,
#     }

#     # Constructing a response dict
#     response_data = {
#         "status_code": status_code,
#         "request_id": request_id,
#         "member_info": member_info,
#         "session_token": session_token,
#         "session_jwt": session_jwt,
#         "organization_info": organization_info,
#     }

#     return response_data
