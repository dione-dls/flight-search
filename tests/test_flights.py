from unittest.mock import Mock, patch

from nose.tools import assert_equal, assert_list_equal, assert_is_none, assert_true

from src.flights import set_requirements, get_flights, get_flight_details

departure_airport = "LGW"
arrival_airport = "BCN"
departure_date = "2019-04-05"
flights_ = {
    'destinations': [
        {
            'arrival': 'BCN',
            'code': 'OD1',
            'departure': 'LGW',
            'flightIds': ['RUo6RmxpZ2h0MQ']
        }
    ],
    'flights': [
        {
            'flightSegments': [
                {
                    'aircraft': {'code': '', 'name': ''},
                    'arrival': {
                        'airportCode': 'BCN',
                        'airportName': '',
                        'date': '2019-04-05',
                        'terminal': 'Terminal 2C',
                        'time': '10:40'
                    },
                    'departure': {
                        'airportCode': 'LGW',
                        'airportName': '',
                        'date': '2019-04-05',
                        'terminal': 'North Terminal',
                        'time': '07:25'
                    },
                    'flightDuration': 0,
                    'flightNumber': '8571',
                    'id': 'U28571',
                    'marketingCarrier': {'airlineId': 'EJ', 'name': 'easyJet'},
                    'operatingCarrier': {'airlineId': 'EJ', 'name': 'easyJet'}
                }
            ],
            'flightSegmentsOrder': ['U28571'],
            'id': 'RUo6RmxpZ2h0MQ'
        }
    ],
    'offers': [
        {
            'expiration': '2019-03-14T22:14:16+0000',
            'journeys': [
                {
                    'destination': 'OD1',
                    'flightIds': ['RUo6RmxpZ2h0MQ']
                }
            ],
            'offerId': 'ZWFzeWpldDo6MTczNzQ1ODQ5NjcwOTg2ODE3',
            'passengers': [
                {
                    'baseAmount': 109,
                    'fares': [
                        {
                            'availableSeats': '9',
                            'code': 'Y',
                            'fareBasisCode': 'Y',
                            'fareCode': 'Y',
                            'fareRefCode': [],
                            'flightSegment': 'U28571',
                            'name': 'BASE',
                            'pcrId': 'PCR_1'
                        }
                    ],
                    'passengerId': 'SH1',
                    'taxAmount': 13,
                    'totalAmount': 122,
                    'type': 'ADT'
                }
            ],
            'provider': 'EJ',
            'totalPrice': {'amount': 122, 'currencyCode': 'GBP'}
        }
    ]
}

all_flights = [
    [
        {
            'airline': 'easyJet',
            'departure_airport': 'LGW',
            'departure_date': '2019-04-05',
            'departure_time': '07:25',
            'arrival_airport': 'BCN',
            'arrival_date': '2019-04-05',
            'arrival_time': '10:40'
        },
        {
            'currency': 'GBP',
            'price': '122'
        }
    ]
]


def test_set_requirements():
    expected_payload = {
        "journeys": [
            {
                "departureAirport": "LGW",
                "arrivalAirport": "BCN",
                "departureDate": "2019-04-05",
                "ticketTypes": [
                    "economy"
                ]
            },
        ],
        "passengers": [
            {
                "type": "adult"
            }
        ]
    }

    result = set_requirements(departure_airport, arrival_airport, departure_date)
    assert_equal(result, expected_payload)


@patch("src.flights.requests.post")
def test_get_flights_when_response_is_ok(mock_post):
    mock_post.return_value = Mock(ok=True)
    mock_post.return_value.json.return_value = [flights_]

    response = get_flights(departure_airport, arrival_airport, departure_date)
    assert_list_equal(response, [flights_])


@patch("src.flights.requests.post")
def test_get_flights_when_response_is_not_ok(mock_post):
    mock_post.return_value.ok = False

    response = get_flights(departure_airport, arrival_airport, departure_date)
    assert_is_none(response)


@patch("src.flights.get_flights")
def test_get_flight_details_when_flights_is_not_none(mock_get_flights):
    mock_get_flights.return_value = Mock()
    mock_get_flights.return_value = flights_

    results = get_flight_details(departure_airport, arrival_airport, departure_date)
    assert_true(mock_get_flights.called)

    assert_list_equal(results, all_flights)
