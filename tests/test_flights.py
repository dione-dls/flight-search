from nose.tools import assert_equal

from flights import set_requirements

departure_airport = "LGW"
arrival_airport = "BCN"
departure_date = "2019-04-05"


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
