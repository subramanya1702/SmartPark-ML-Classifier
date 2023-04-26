import json

import boto3

client = boto3.resource('dynamodb')


def lambda_handler(event, context):
    print(event)
    responseObject = {}

    if 'pathParameters' not in event or 'latitude' not in event['pathParameters'] or 'longitude' not in event[
        'pathParameters']:
        responseObject["statusCode"] = 400
        responseObject["headers"] = {}
        responseObject["headers"]["Content-Type"] = "error"
        responseObject["body"] = "Latitude and Longitude cannot be empty"

        return responseObject

    latitude = event['pathParameters']['latitude']
    longitude = event['pathParameters']['longitude']

    last_added_parking_lot_table = client.Table('LastAddedParkingLot')
    last_added_parking_lot_response = last_added_parking_lot_table.get_item(
        Key={
            'latlon': str(latitude) + ':' + str(longitude)
        }
    )

    if 'Item' not in last_added_parking_lot_response:
        print("ERROR: Item object not found in last added parking lot response")
        responseObject["statusCode"] = 500
        responseObject["headers"] = {}
        responseObject["headers"]["Content-Type"] = "error"
        responseObject["body"] = "Internal Server Error"

        return responseObject

    timestamp = last_added_parking_lot_response['Item']['timestamp']
    parking_lot_table = client.Table('ParkingLotLog')
    parking_lot_response = parking_lot_table.get_item(
        Key={
            'latlon': str(latitude) + ':' + str(longitude),
            'timestamp': timestamp
        }
    )

    if 'Items' not in parking_lot_response:
        print("ERROR: Items object not found in parking lot response")
        responseObject["statusCode"] = 500
        responseObject["headers"] = {}
        responseObject["headers"]["Content-Type"] = "error"
        responseObject["body"] = "Internal Server Error"

        return responseObject

    recent_record = parking_lot_response['Items'][0]
    dynamodb_response = {
        "parking_lot_name": recent_record['parking_lot_name'],
        "number_of_empty_parking_slots": int(recent_record['empty_parking_spaces']),
        "total_number_of_parking_lots": int(recent_record['total_parking_spaces']),
        "timestamp": recent_record['timestamp'],
        "image_url": recent_record['image_url'],
        "parking_lot_time_limit": recent_record['parking_lot_time_limit'],
        "parking_charges": recent_record['parking_charges']
    }

    # Creating a HTTP response object
    responseObject["statusCode"] = 200
    responseObject["headers"] = {}
    responseObject["headers"]["Content-Type"] = "application/json"
    responseObject["body"] = json.dumps(dynamodb_response)
    print(responseObject)

    return responseObject
