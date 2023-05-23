import datetime
import json

import boto3

client = boto3.resource('dynamodb')
required_fields = ["parking_lot_name", "empty_parking_spaces", "total_parking_spaces", "timestamp",
                   "original_image_url", "parking_lot_time_limit", "parking_charges"]


def lambda_handler(event, context):
    print(event)
    response_object = {}

    all_parking_lots_table = client.Table('AllParkingLots')
    all_parking_lots_response = all_parking_lots_table.scan()

    if 'Items' not in all_parking_lots_response:
        print("ERROR: Items object not found in all parking lots response\n")
        print(all_parking_lots_response)

        return get_error_response_object(response_object)

    dynamodb_responses = []
    for item in all_parking_lots_response['Items']:
        if validate_dynamodb_response(item):
            print("Required field(s) missing in the dynamodb response.")
            return get_error_response_object(response_object)

        latlon = item['latlon'].split(':')
        dynamodb_response = {
            "latitude": latlon[0],
            "longitude": latlon[1],
            "parking_lot_name": item['parking_lot_name'],
            "number_of_empty_parking_slots": int(item['empty_parking_spaces']),
            "total_number_of_parking_lots": int(item['total_parking_spaces']),
            "timestamp": str(datetime.datetime.fromtimestamp(int(item['timestamp']))),
            "image_url": item['original_image_url'],
            "parking_lot_time_limit": item['parking_lot_time_limit'],
            "parking_charges": int(item['parking_charges'])
        }
        dynamodb_responses.append(dynamodb_response)

    response_object["statusCode"] = 200
    response_object["headers"] = {}
    response_object["headers"]["Content-Type"] = "application/json"
    response_object["body"] = json.dumps({"parkingLots": dynamodb_responses})
    print(response_object)

    return response_object


def get_error_response_object(response_object):
    response_object["statusCode"] = 500
    response_object["headers"] = {}
    response_object["headers"]["Content-Type"] = "error"
    response_object["body"] = "Internal Server Error"

    return response_object


def validate_dynamodb_response(item):
    is_not_valid = False

    for field in required_fields:
        if field not in item:
            print("ERROR: Field: {0} is missing in item: {1}\n".format(field, item))
            is_not_valid = True

    return is_not_valid
