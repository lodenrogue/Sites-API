from flask import Flask, Response
from flask_cors import CORS
import requests
import json

SITES_DATA_API = 'http://api.sfwmd.gov/v1/data/realtime?format=json'
CENTRAL_REGISTRATION_API = 'http://api.sfwmd.gov/v1/crs/site'

app = Flask(__name__)
CORS(app)


@app.route('/water/api/v1/sites/<site_name>', methods=['GET'])
def get_site(site_name):
    site_name = site_name.upper()
    site = get_site_by_name(site_name)

    # If site was not found return a 404
    if site is None:
        resp = Response(status=404, mimetype='application/json')

    # Else return the site
    else:
        js = json.dumps(site)
        resp = Response(js, status=200, mimetype='application/json')

    return resp


# Encode ampersand
def encode_site(site_name):
    return site_name.replace('&', '%26')


# Find a site by name and return a reformatted version of the response
def get_site_by_name(site_name):
    encoded_site = encode_site(site_name)
    r = requests.get(url=SITES_DATA_API + '&sites=' + encoded_site)
    json_response = r.json()

    # Create site
    site = dict()
    site['name'] = site_name
    site['pumps'] = []
    site['gates'] = []
    site['flows'] = []
    site['headwaters'] = []
    site['tailwaters'] = []
    site['stages'] = []
    site['rainfall'] = []
    site['tiltmeterTemperatures'] = []
    site['tiltmeterRotationDeflection'] = []

    # Get timeseries response and check if it the site was not found
    timeseries_response = json_response.get('timeSeriesResponse')
    if timeseries_response.get('status').get('statusCode') == 1:
        return None

    with open('sites.json') as f:
        sites_metadata = json.load(f)

    # Get Lat/Long
    for s_meta in sites_metadata.get('sites').get('site'):
        if s_meta.get('siteName') == site_name:
            site['latitude'] = s_meta.get('latitude')
            site['longitude'] = s_meta.get('longitude')
            site['createdDate'] = s_meta.get('createdDate')
            site['status'] = s_meta.get('status')
            break

    # Iterate through timeseries array and create objects
    for timeseries in timeseries_response.get('timeSeries'):
        # Get description
        source_info = timeseries.get('sourceInfo')
        site['description'] = source_info.get('siteName')

        # Get parameter metadata
        name = timeseries.get('name')
        application_name = timeseries.get('applicationName')

        # Get parameter
        parameter = timeseries.get('parameter')
        parameter_name = parameter.get('parameterName')

        # Get unit of measure
        unit = parameter.get('unit')
        unit_code = unit.get('unitCode')

        # Get value
        timeseries_value = timeseries.get('values')[0]
        value = timeseries_value.get('value')
        date_time = timeseries_value.get('dateTime')
        quality_code = timeseries_value.get('qualityCode')

        # Create object
        object = {
            'name': name,
            'applicationName': application_name,
            'unitCode': unit_code,
            'value': value,
            'qualityCode': quality_code,
            'dateTime': date_time
        }

        # Pump
        if parameter_name == 'PUMP':
            site['pumps'].append(object)

        # Gates
        elif parameter_name == 'GATE OPENING':
            site['gates'].append(object)

        # Flow
        elif parameter_name == 'FLOW':
            site['flows'].append(object)

        # Headwater
        elif parameter_name == 'HEADWATER ELEVATION':
            site['headwaters'].append(object)

        # Tailwater
        elif parameter_name == 'TAILWATER ELEVATION':
            site['tailwaters'].append(object)

        # Stage
        elif parameter_name == 'STAGE':
            site['stages'].append(object)

        # Rainfall
        elif parameter_name == 'RAINFALL':
            site['rainfall'].append(object)

        # Tiltmeter Temperature
        elif parameter_name == 'TILTMETER TEMPERATURE':
            site['tiltmeterTemperatures'].append(object)

        # Tiltmeter Rotation, Deflection
        elif parameter_name == 'TILTMETER ROTATION, DEFLECTION':
            site['tiltmeterRotationDeflection'].append(object)

    return site


# Finds and builds a list of sites that have no data in the data api
def find_null_sites():
    # Get all sites to search by name
    with open('sites.json', 'r') as sj:
        sites_json = json.loads(sj.read())

    # Get the null values list
    with open('NULL_VALUES.txt', 'r') as nv:
        null_values = nv.read().split('\n')

    # For each site, get the response and if its None then
    # add it to the null values list
    for site in sites_json.get('sites').get('site'):
        site_name = site.get('siteName')

        if site_name not in null_values:
            site = get_site_by_name(site_name)

            if site is None:
                with open('NULL_VALUES.txt', 'a') as nv:
                    nv.write(site_name + '\n')
                    print(site_name, 'was not found')


if __name__ == '__main__':
    app.run()
