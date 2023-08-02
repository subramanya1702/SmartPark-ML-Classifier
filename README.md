# Smart-Park-Reboot

## Overview

This work is based on [Sriranga Chaitanya Nandam's Master's Project](https://research.engr.oregonstate.edu/si-lab/#archive):
* [PDF](https://research.engr.oregonstate.edu/si-lab/archive/2022_chaitanya.pdf)
* [Github](https://github.com/NSR9/Smart-Park)

Ingress and egress pipelines developed by Chaitanya, have undergone modifications to enhance their performance and scalability. 
The ingress pipeline has been refactored to insert data into a MongoDb database and is now executed as a Docker container.
Likewise, the egress pipeline, which was previously hosted on AWS using technologies like Lambda and API Gateway, has been migrated to a simpler NodeJs server, tasked with fetching data from MongoDb.
Both pipelines, along with the MongoDb, are now bundled and executed as Docker containers.

Below is a reworked architecture diagram.

## Architecture Diagram
![Architecture_Diagram.png](Architecture_Diagram.png)

## Usage
The usage instructions have been split into two parts, depending on whether one has an Oregon State University account or not.

#### Oregon State University access

Continue with this section if you have an Oregon State University account and have access to this Box [folder](https://oregonstate.box.com/s/9evjdwny12h28lar4cyp8s02zouj195i).
If not, jump ahead to the [next](#non-oregon-state-university-access) section.

1. Ensure you are on a system with x86 architecture and Linux operating system
2. System has at least 2GB of RAM and 24GB of disk space
3. Download the latest ML classifier (spclassifier) tar archive file from the ML Classifier Box folder over [here](https://oregonstate.box.com/s/9evjdwny12h28lar4cyp8s02zouj195i)
4. Unzip the tar archive
    ```sh
    tar -xzvf <filename>.tar.gz
    ```

5. Build a docker image from the tar archive
   ```sh
   docker load --input <filename>.tar
   ```

6. Confirm whether the image has been created successfully by executing the following command
    ```sh
    docker images
    ```

7. Run a docker container using the newly generated image. The command will launch a new container in detached mode.
    ```sh
    docker run -d --env DB_CONN_STR=HOSTNAME --name spclassifier --restart always <image_name>
    ```
   DB_CONN_STR is the mongodb connection string that needs to be passed as an environment variable to the container.
   Example:

    * Using database server's DNS: `DB_CONN_STR=db.domain.com:{port}`
    * Using database server's public/external IP: `DB_CONN_STR=x.x.x.x:{port}`
    * Testing locally: `DB_CONN_STR=localhost:{port}` or `DB_CONN_STR=127.0.0.1:{port}`

8. Inspect the container logs and verify if the pipeline is running without any errors
    ```sh
    docker logs -f --tail 500 spclassifier
    ```

9. Log in to the MongoDb container and verify if records are getting inserted into `recentParkingLots`
   and `parkingLotHistory` collections.

#### Non Oregon State University access

1. Ensure that you are on a Linux system with x86 architecture. If you don’t have access to one, follow the below
   instructions.
   Note: These instructions assume that you will be using AWS as the cloud service provider. Skip this step if you are
   using a different provider.
    1. Go to EC2 console in AWS
    2. Create a new instance with the following configuration
        1. Name: MLClassifier
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
3. Clone the SmartPark-ML-Classifier repository from [here](https://github.com/subramanya1702/SmartPark-ML-Classifier)
   and navigate to `SmartPark-ML-Classifier/smart_park` folder.
4. Download the pytorch file: X-512.pt from [here](https://oregonstate.box.com/s/zhurkyxoxghmfp77fsjgp33rflc37jaq)
5. Now that everything is set up, we can go ahead and build a docker image
    ```sh
    sudo docker build -t spclassifier .
    ```

6. Copy the image to wherever necessary/convenient.
7. Run a docker container using the newly copied image. The command will launch a new container in detached mode.
    ```sh
    sudo docker run -d --env DB_CONN_STR=HOSTNAME --name spclassifier --restart always spclassifier
    ```
   DB_CONN_STR is the mongodb connection string that needs to be passed as an environment variable to the container.
   Example:

    * Using database server's DNS: `DB_CONN_STR=db.domain.com:{port}`
    * Using database server's public/external IP: `DB_CONN_STR=x.x.x.x:{port}`
    * Testing locally: `DB_CONN_STR=localhost:{port}` or `DB_CONN_STR=127.0.0.1:{port}`

8. Log in to the MongoDb container and verify if records are getting inserted into `recentParkingLots`
   and `parkingLotHistory` collections.
9. Don't forget to deallocate any resources that were provisioned on AWS.

## Contributors
Subramanya Keshavamurthy
