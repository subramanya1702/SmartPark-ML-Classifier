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
    docker run -d --env DB_CONN_STR=HOSTNAME --name spclassifier --restart always <image_name>
    ```
    DB_CONN_STR is an optional environment variable that has to be passed when the node js application and database are running on different
    servers.
    If not, it can be skipped.
    Example:
    
    * Using database server's DNS: `DB_CONN_STR=db.domain.com:{port}`
    * Using database server's public/external IP: `DB_CONN_STR=x.x.x.x:{port}`

9. Inspect the container logs and verify if the pipeline is running without any errors
    ```sh
    docker logs -f --tail 500 spclassifier
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
3. Clone the SmartPark repository from [here](https://github.com/subramanya1702/Smart-Park-Reboot).
4. Now that everything is set up, we can go ahead and create/build a docker image
    ```sh
    sudo docker build -t spclassifier .
    ```
5. Copy the image to wherever necessary/convenient.
6. Run a docker container using the newly copied image. The command will launch a new container in detached mode.
    ```sh
    sudo docker run -d --env DB_CONN_STR=HOSTNAME --name spclassifier --restart always spclassifier
    ```
    DB_CONN_STR is an optional environment variable that has to be passed when the node js application and database are running on different
    servers.
    If not, it can be skipped.
    Example:
    
    * Using database server's DNS: `DB_CONN_STR=db.domain.com:{port}`
    * Using database server's public/external IP: `DB_CONN_STR=x.x.x.x:{port}`

7. Don't forget to deallocate any resources that were provisioned on AWS.

## Contributors
Subramanya Keshavamurthy
