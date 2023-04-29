import datetime
import json

import boto3

client = boto3.resource('dynamodb')


def lambda_handler(event, context):
    print(event)
    response_object = {}

    all_parking_lots_table = client.Table('AllParkingLots')
    all_parking_lots_response = all_parking_lots_table.scan()

    if 'Items' not in all_parking_lots_response:
        print("ERROR: Items object not found in all parking lots response")
        print(all_parking_lots_response)

        response_object["statusCode"] = 500
        response_object["headers"] = {}
        response_object["headers"]["Content-Type"] = "error"
        response_object["body"] = "Internal Server Error"

        return response_object

    dynamodb_responses = []
    for item in all_parking_lots_response['Items']:
        dynamodb_response = {
            "parking_lot_name": item['parking_lot_name'],
            "number_of_empty_parking_slots": int(item['empty_parking_spaces']),
            "total_number_of_parking_lots": int(item['total_parking_spaces']),
            "timestamp": str(datetime.datetime.fromtimestamp(int(item['timestamp']))),
            "image_url": item['image_url'],
            "parking_lot_time_limit": item['parking_lot_time_limit'],
            "parking_charges": item['parking_charges']
        }
        dynamodb_responses.append(dynamodb_response)

    response_object["statusCode"] = 200
    response_object["headers"] = {}
    response_object["headers"]["Content-Type"] = "application/json"
    response_object["body"] = json.dumps({"parkingLots": dynamodb_responses})
    print(response_object)

    return response_object
