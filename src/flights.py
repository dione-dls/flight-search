#!/usr/bin/env python
from urllib.parse import urljoin

import requests
import sys

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


def get_flights(departure_airport, arrival_airport, departure_date):
    payload = set_requirements(departure_airport, arrival_airport, departure_date)
    response = requests.post(FLIGHTS_URL, headers=HEADER, json=payload)
    if response.ok:
        return response.json()
    else:
        return None


def get_flight_details(departure_airport, arrival_airport, departure_date):
    available_flights = get_flights(departure_airport, arrival_airport, departure_date)
    all_flights = []

    if available_flights is not None:
        flights = available_flights["flights"]
        flight_ids = available_flights["destinations"][0]["flightIds"]
        for flight_id in flight_ids:
            for flight in flights:
                if flight_id == flight["id"]:
                    segments = []
                    for flight_segment in flight["flightSegments"]:
                        segments.append(
                            {
                                "airline": flight_segment["marketingCarrier"]["name"],
                                "departure_airport": flight_segment["departure"]["airportCode"],
                                "departure_date": flight_segment["departure"]["date"],
                                "departure_time": flight_segment["departure"]["time"],
                                "arrival_airport": flight_segment["arrival"]["airportCode"],
                                "arrival_date": flight_segment["arrival"]["date"],
                                "arrival_time": flight_segment["arrival"]["time"],
                            }
                        )
                    offers = available_flights["offers"]
                    for offer in offers:
                        if flight_id == offer["journeys"][0]["flightIds"][0]:
                            segments.append(
                                {
                                    "currency": offer["totalPrice"]["currencyCode"],
                                    "price": str(offer["totalPrice"]["amount"]),
                                }
                            )
                            all_flights.append(segments)

        return all_flights


def show_flights(departure_airport, arrival_airport, departure_date):
    flights_ = get_flight_details(departure_airport, arrival_airport, departure_date)

    print("-" * 100)
    print(f"Flights from {departure_airport} to {arrival_airport} on {departure_date}")
    print("-" * 100)

    for flight in flights_:
        for info in flight:
            print(
                "     ".join(
                    filter(
                        None, (info.get('airline'),
                               info.get('departure_airport'),
                               info.get('departure_date'),
                               info.get('departure_time'),
                               info.get('arrival_airport'),
                               info.get('arrival_date'),
                               info.get('arrival_time'),
                               info.get('currency'),
                               info.get('price'),
                               )
                    )
                )
            )
        print("-" * 100)


if __name__ == '__main__':
    show_flights(*sys.argv[1:])

