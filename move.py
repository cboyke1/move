#!/usr/bin/env python3
import requests, re, configparser, boto3, botocore, sys

def main():
	new_ip=get_my_ip()
	
	config=configparser.ConfigParser()
	config.optionxform=str
	config.read('move.ini')

	old_ip=config['ip'].get('old_ip')
	
	envs = config.get('aws','envs').split(',')
	for env in envs:
		profile = config.get(env,'profile')
		
		# Fetch a session specific to this AWS profile
		session=boto3.Session(profile_name=profile)
		client=session.client('ec2')

		if old_ip == None:
			print('no old IP')
		else:
			revoke_old_ip(client,config,env,old_ip)
		
		grant_new_ip(client,config,env,new_ip)

		save_new_ip_as_old(config,new_ip)

			
def get_my_ip():
	user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}
	r = requests.get("https://ipcow.com/", headers=user_agent)
	if r.status_code==200:
		m=re.search('<span id="lblUserIP">(.*?)</span>',r.text)
		if m:
			new_ip=m.group(1)
			print('My IP is:',new_ip)
			return new_ip
	else:
		print('Status',r.status_code)

def revoke_old_ip(client,config,env,ip):
	groups = config.get(env,'groups').split(',')
	for group in groups:
		print('revoking',ip,'from',env,'group',group)
		try:
			client.revoke_security_group_ingress(GroupId=group,IpPermissions=[
				{	'FromPort':-1,
					'ToPort':-1,
					'IpProtocol':'-1',
					'IpRanges':[
						{
							'CidrIp': ip+'/32'
						}
					]
				}])
		except Exception as e:
			print(e)
		
def grant_new_ip(client,config,env,ip):
	
	groups = config.get(env,'groups').split(',')
	for group in groups:
		print('granting',ip,'in',env,'group',group)
		try:
			response = client.authorize_security_group_ingress(GroupId=group,IpPermissions=[
				{	'FromPort':-1,
					'ToPort':-1,
					'IpProtocol':'-1',
					'IpRanges':[
						{
							'CidrIp': ip+'/32',
							'Description': config.get('access','description')
						}
					]
				}])
		except Exception as e:
			print(e)

	
def save_new_ip_as_old(c,new_ip):
	c.set('ip','old_ip',new_ip)
	with open("move.ini",'w') as f:
		c.write(f)
	
main()

