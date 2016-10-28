# Sites-API
A better implementation of the SFWMD Sites API

===

### How to use
#### Expected input 

GET: /water/api/v1/sites/{siteName}

#### Expected output

Status: 200 OK

~~~
{
  "name": "S6",
  "description": "S6 PUMP STATION",
  "latitude": 26.472018864719,
  "longitude": -80.445328155019,
  "status": "A",
  "createdDate": "2015-07-14 22:00:24.0",
  "headwaters": [
    {
      "applicationName": "SG3",
      "dateTime": "2016-08-22T06:31:00:000",
      "name": "S6@H",
      "qualityCode": "P",
      "unitCode": "ft NGVD29",
      "value": 9.61
    },
    ...
  ],
  "tailwaters": [
    {
      "applicationName": "SG4",
      "dateTime": "2016-10-28T03:47:00:000",
      "name": "S6-T",
      "qualityCode": "P",
      "unitCode": "ft NGVD29",
      "value": 13.135
    },
    ...
  ],
  "pumps": [
    {
      "applicationName": "SG4",
      "dateTime": "2016-10-28T03:47:00:000",
      "name": "S6P-1",
      "qualityCode": "P",
      "unitCode": "rpm",
      "value": 0
    },
    ...
  ],
  "flows": [
    {
      "applicationName": "SG4",
      "dateTime": "2016-10-28T03:47:00:000",
      "name": "S6-P-Q2",
      "qualityCode": "P",
      "unitCode": "cfs",
      "value": 0
    },
    ...
  ],
  "rainfall": [
    {
      "applicationName": "SG4",
      "dateTime": "2016-10-28T03:47:00:000",
      "name": "S6-R",
      "qualityCode": "P",
      "unitCode": "INCHES",
      "value": 0
    }
  ],
  "stages": [],
  "gates": [],
  "tiltmeterTemperatures": [],
  "tiltmeterRotationDeflection": []
}
~~~

Definitions:

| Key                         | Type   | Definition                                                                 |
|-----------------------------|--------|----------------------------------------------------------------------------|
| name                        | String | Name of the site                                                           |
| description                 | String | Description of the site                                                    |
| latitude                    | Float  | Latitude coordinate of the site's location                                 |
| longitude                   | Float  | Longitude coordinate of the site's location                                |
| status                      | String | Status of the site. 'A' is active, 'I' is inactive, and 'D' is deactivated |
| createdDate                 | String | Date when the site was created                                             |
| headwaters                  | Array  | An array containing the headwater measurements                             |
| tailwaters                  | Array  | An array containing the tailwater measurements                             |
| pumps                       | Array  | An array containing the pump measurements                                  |
| flows                       | Array  | An array containing the flow measurements                                  |
| rainfall                    | Array  | An array containing the rainfall measurements                              |
| stages                      | Array  | An array containing the stage measurements                                 |
| gates                       | Array  | An array containing the gate measurements                                  |
| tiltmeterTemperatures       | Array  | An array containing the tiltmeter temperature measurements                 |
| tiltmeterRotationDeflection | Array  | An array containing the tiltmeter rotation deflection measurements         |
