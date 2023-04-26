import configparser

config = configparser.ConfigParser()

# All the below config params might change based on the new configuration of the EC2 instance, Mongodb instance and
# AWS account creds. Please update with your own if this doesnt work.


# Add the structure to the file we will create
config.add_section('MODEL_INPUTS')
config.set('MODEL_INPUTS', 'weights', '/home/ubuntu/urban-detection/yolov5/weights/S-512.pt')
config.set('MODEL_INPUTS', 'source',
           '/home/ubuntu/urban-detection/yolov5/pre_processed_images/2022-10-25T19:01:05.471217_r40ko8z.jpg')
config.set('MODEL_INPUTS', 'output', '/home/ubuntu/urban-detection/inference/output')
config.set('MODEL_INPUTS', 'img-size', '512')
config.set('MODEL_INPUTS', 'conf-thres', '0.4')
config.set('MODEL_INPUTS', 'iou-thres', '0.5')
config.set('MODEL_INPUTS', 'device', '')
config.set('MODEL_INPUTS', 'view-img', 'False')
config.set('MODEL_INPUTS', 'save-txt', 'False')
config.set('MODEL_INPUTS', 'classes', 'None')
config.set('MODEL_INPUTS', 'agnostic-nms', 'False')
config.set('MODEL_INPUTS', 'augment', 'False')
config.set('MODEL_INPUTS', 'update', 'False')
config.set('MODEL_INPUTS', 'fixed-colors', 'False')
config.set('MODEL_INPUTS', 'ped-count', 'False')

config.add_section('AWS_CREDS')
# set these by contacting the REPO owner


config.add_section('AWS_ENV')
# These might change if the instance is recreated and restarted
config.set('AWS_ENV', 'S3_BUCKET_NAME', 'detectionlog')
config.set('AWS_ENV', 'S3_OBJECT_NAME', 'prediction_images/')

config.add_section('PRE_PROCESSING_BOUNDS')
config.set('PRE_PROCESSING_BOUNDS', 'x-coordinate', '0')
config.set('PRE_PROCESSING_BOUNDS', 'y-coordinate', '658')
config.set('PRE_PROCESSING_BOUNDS', 'height', '420')
config.set('PRE_PROCESSING_BOUNDS', 'width', '1918')

# Write the new structure to the new file
with open(r"configfile.ini", 'w') as configfile:
    config.write(configfile)
