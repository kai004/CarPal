from flask import Flask
from flask import render_template
from flask import request

from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

import smartcar

client = smartcar.AuthClient(
	client_id = 'ea6bdfac-493e-41bf-ad40-2d8230d2130a',
	client_secret = '2b970c69-3698-45f7-883f-b7b505f8a925',
	redirect_uri = 'http://localhost:5000/after-auth',
)

app = Flask(__name__)
GoogleMaps(app, key="AIzaSyD4-8cGahf7ABQ34z66Pq1c2B6GOEr1Gec")

@app.route('/')
def index():
    return "Currently on the index page. /smartcar for smartcar auth. UPDATED"

@app.route('/smartcar')
def smartcar_auth():
	auth_url = client.get_auth_url()

	link = auth_url
	return render_template('smartcar.html', link=link)

@app.route('/maps')
def maps_test():

	latitude = 34.0699
	longitude = -118.4466
	mymap = Map(
	        identifier="view-side",
	        lat= latitude,
	        lng= longitude,
	        markers=[(latitude, longitude)]
	)
	return render_template('maps.html', mymap=mymap, lat=latitude, lng=longitude)


@app.route('/after-auth', methods=['GET'])
def after_auth():
	if request.method == 'GET':
		auth_code = request.args.get('code', None)
		access = client.exchange_code(auth_code)
		access_token = access['access_token']

		print(access)
		response = smartcar.get_vehicle_ids(access['access_token'])

		print(response)

		vid = response['vehicles'][0]

		print(vid)

		vehicle = smartcar.Vehicle(vid, access_token)

		location = vehicle.location()

		print(location)

		return render_template('after_auth.html', code=auth_code, lat=location['data']['latitude'], lon=location['data']['longitude'])

if __name__ == "__main__":
	app.run()
