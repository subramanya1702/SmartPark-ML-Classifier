# Smart-Park-Reboot

This work is based on [Sriranga Chaitanya Nandam's Master's Project](https://research.engr.oregonstate.edu/si-lab/#archive):
* [PDF](https://research.engr.oregonstate.edu/si-lab/archive/2022_chaitanya.pdf)
* [Github](https://github.com/NSR9/Smart-Park)

## Getting Started

The ingress pipeline, developed by Chaitanya initially, has been modified to run as a Docker container after packaging.
The egress pipeline has also undergone modifications to retrieve data from DynamoDb in place of MongoDb. Below is a reworked architecture diagram.


![Architecture_Diagram.png](Architecture_Diagram.png)

## Usage

Note: The following sections guide you through the process of executing the ingress pipeline as a docker container. Depending on the availability of the docker image, you can refer to the respective sections.

#### Docker image is available

1. The server must operate on an x86 architecture with Linux as its operating system.
2. A minimum of 2GB of RAM and 24GB of disk space should be allocated
3. Ensure that the latest version of docker is installed on the server
4. Download the latest Smart Park tar archive file from the box folder here
5. Unzip the tar archive
    ```sh
    tar -xzvf <filename>.tar.gz
    ```
   
6. Now, create a docker image from the tar archive
   ```sh
   docker load --input <filename>.tar
   ```
   
7. Confirm whether the image has been created successfully by executing the following command
    ```sh
    docker images
    ```
   
8. Run a docker container using the newly generated image. The command will launch a new container in detached mode.
    ```sh
    docker run -d --restart always <filename>
    ```

9. Inspect the container logs and verify if the pipeline is running without any errors
    ```sh
    docker logs -f --tail 500 <image-id>
    ```

10. Upon successful completion of the above steps, you should be able to observe new prediction images in detectionlog S3 bucket, as well as new records in the ParkingLotLog DynamoDB table.


#### Docker image is not available

Don’t panic! We have all the resources to create one.

1. Ensure that you are on a Linux system with x86 architecture. If you don’t have access to one, follow the below instructions.
   1. Go to EC2 console in AWS
   2. Create a new instance with the following configuration
      1. Name: SmartPark
      2. AMI: Ubuntu 22.04
      3. Architecture: 64-bit x86
      4. Type: t2.small
      5. Create a new key pair or select an existing one
      6. In network settings, select the default VPC (Create a new one if you want)
      7. Enable Auto assign public IP
      8. Create a new security group and allow SSH traffic from your IP
      9. In Storage settings, allocate a minimum of 24GiB of gp2 storage
      10. Launch the instance
      11. Connect to the instance through SSH
2. Install docker by following the instructions [here](https://docs.docker.com/engine/install/ubuntu/)
3. Clone the SmartPark repository from [here](https://github.com/subramanya1702/Smart-Park-Reboot). Before proceeding further, we need to make changes to a config file. Open SmartPark folder that you just cloned and navigate to smart_park → config. Open config.yml file and replace the following properties with your AWS account’s BASE64 encoded access and secret keys. (This [tool](https://www.base64encode.org/) might be helpful)
    ```sh
    aws:
      credentials:
        access_key: <BAS64_ENCODED_ACCESS_KEY>
        secret_key: <BAS64_ENCODED_SECRET_KEY>
    ```
    If you are doing this on a remote server(EC2), copy the SmartPark repository from your local machine to the remote server (scp utility will be helpful). You can of course clone the repository in the remote server, but you would have to go through the pain of installing git and configuring your credentials for it to work. So, copying from your local machine is a better choice.

4. Now that everything is set up, we can go ahead and create/build a docker image
    ```sh
    sudo docker build -t <image_name> .
    ```
   
5. Run a docker container using the newly created image. The command will launch a new container in detached mode.
    ```sh
    sudo docker run -d --restart always <image_name>
    ```

6. Verify if the prediction images are getting uploaded to S3 bucket detectionlog and new records are being inserted to DynamoDB table ParkingLotLog.

7. You are all set!

## Contributors
Subramanya Keshavamurthy
