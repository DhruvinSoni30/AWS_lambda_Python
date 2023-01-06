import os
import boto3
import json_operations 
import json

# loading data from JSON 
config_data = json_operations.loadJsonData("config.json")
key_path = config_data["key_path"]
key_name = config_data["key_name"]
ami_id = config_data["ami_id"]
instance_type = config_data["instance_type"]
region_name = config_data["region_name"]
ec2_json_data_path = config_data["ec2_data_path"]

ec2_client = boto3.client("ec2", region_name=region_name)

# create key_pair for EC2 instance
def create_key_pair():
    if not os.path.exists(key_path):
        key_pair = ec2_client.create_key_pair(KeyName=key_name)
        private_key = key_pair["KeyMaterial"]
        # writing the key & changing it's permission to 400
        with os.fdopen(os.open(key_path, os.O_WRONLY | os.O_CREAT, 0o400), "w+") as handle:
            handle.write(private_key)
create_key_pair()

# create EC2 Instance
def create_instance():
    instances = ec2_client.run_instances(
        ImageId = ami_id,
        MinCount = 3,
        MaxCount = 3,
        InstanceType = instance_type,
        KeyName =  key_name,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name','Value': 'Linux Server'},{'Key': 'Env','Value': 'Prod'}]
            }
        ]
    )
    for i in instances['Instances']:
        print("Instance ID Created is :{} Instance Type Created is : {}" .format(i['InstanceId'],i['InstanceType']))
create_instance()
