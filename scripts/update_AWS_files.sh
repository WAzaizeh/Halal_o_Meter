#-- start config
# Local Directory from which files will be copied
LD1=/Users/wesamazaizeh/Desktop/Projects/halal_o_meter/web
LD2=/Users/wesamazaizeh/Desktop/Projects/halal_o_meter/docker
LD3=/Users/wesamazaizeh/Desktop/Projects/halal_o_meter/data
LD4=/Users/wesamazaizeh/Desktop/Projects/halal_o_meter/docker-compose.yml
LD5=/Users/wesamazaizeh/Desktop/Projects/halal_o_meter/logo

# Path to SSH ID file (private key)
ID=/Users/wesamazaizeh/Desktop/AWS_keys/aws_ec2_streamlit.pem

# USERname to login as
USER=ec2-user

#HOST to login to
HOST=ec2-3-22-170-223.us-east-2.compute.amazonaws.com
#--- end config

sudo scp -ri $ID $LD1 $LD2 $LD3 $LD4 $LD5 $USER@$HOST:~/app/
