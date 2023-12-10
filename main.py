# This file will need to use the DataManager,FlightSearch, FlightData,
# NotificationManager classes to achieve the program requirements.

from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from datetime import date, timedelta
import os

SHEETY_TOKEN = os.environ.get('sheety_token')
SHEETY_ENDPOINT = os.environ.get('sheety_endpoint')
TEQUILA_TOKEN = os.environ.get('sheety_token')
TEQUILA_ENDPOINT = 'https://api.tequila.kiwi.com'
TWILIO_SID = os.environ.get('twilio_account_sid')
TWILIO_TOKEN = os.environ.get('twilio_token')
TWILIO_PHONE_NO = os.environ.get('twilio_phone_no')
DESTINATION_PHONE_NO = os.environ.get('destination_phone_no')
ORIGIN_CITY_IATA = "LON"

data_manager = DataManager(SHEETY_ENDPOINT, SHEETY_TOKEN)
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch(TEQUILA_ENDPOINT, TEQUILA_TOKEN)
notification_manager = NotificationManager(TWILIO_SID, TWILIO_TOKEN)
start_date = date.today() + timedelta(days=1)
end_date = start_date + timedelta(days=180)

if not any(x['iataCode'] != '' for x in sheet_data):  # if the iataCodes are all empty
    for index, data in enumerate(sheet_data):
        sheet_data[index]['iataCode'] = flight_search.get_destination_code(data['city'])
    data_manager.destination_data = sheet_data
    data_manager.update_destination_data()

for destination in sheet_data:
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=start_date,
        to_time=end_date
    )
    if flight.price < int(destination['lowestPrice']):
        text = f'Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."'
        notification_manager.send_sms(TWILIO_PHONE_NO, DESTINATION_PHONE_NO, text)


