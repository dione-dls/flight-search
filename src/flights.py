#!/usr/bin/env python
from urllib.parse import urljoin

from constants import BASE_URL, API_KEY

FLIGHTS_URL = urljoin(BASE_URL, 'flights/search')
HEADER = {"x-api-key": API_KEY}


def set_requirements(departure_airport, arrival_airport, departure_date):
    payload = {
        "journeys": [
            {
                "departureAirport": departure_airport,
                "arrivalAirport": arrival_airport,
                "departureDate": departure_date,
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

    return payload
