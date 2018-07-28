# move.py #

Allows you to move around the country and stay close to the things that matter most:  your beloved EC2 instances!

<b>move.py</b> uses www.ipcow.com to grab your current publicly visible IP address, and then grants access to that IP with the specified AWS security group (or groups).  It also cleans up after itself by revoking access from a prior IP address (it saves the prior IP to the .ini file on every run).

## Prerequisites ##

<b>move.py</b> uses the Python <a href="https://boto3.readthedocs.io/en/latest/">boto3</a> library and assumes you have an aws cli configuration set up with permissions to modify security groups in your environment.
