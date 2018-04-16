import patreon
from urlparse import urlparse, parse_qs

# Get your token here: https://www.patreon.com/portal/registration/register-clients
access_token = 'APITOKEN'  # your Creator Access Token
api_client = patreon.API(access_token)

# Get the campaign ID
campaign_response = api_client.fetch_campaign()
campaign_id = campaign_response.data()[0].id()

# Fetch all pledges
pledges = []
cursor = None
while True:
    pledges_response = api_client.fetch_page_of_pledges(campaign_id, 10, cursor=cursor)
    pledges += pledges_response.data()

    # Until this is fixed: https://github.com/Patreon/patreon-python/issues/19
    try:
      cursor = parse_qs(urlparse(pledges_response.json_data['links']['next']).query)['page[cursor]'][0]
    except KeyError:
      break
    # cursor = api_client.extract_cursor(pledges_response)


names_and_pledges = [{
    'email': pledge.relationship('patron').attribute('email'),
    'id': pledge.id(),
    'url': pledge.relationship('patron').attribute('url'),
    'amount_cents': pledge.attribute('amount_cents'),
} for pledge in pledges]

print names_and_pledges

for p in names_and_pledges:
  dollar = str(p['amount_cents'] / 100)
  delim = "\t"
  print p['id'] + delim + p['email'] + delim + dollar + delim + p['url']
