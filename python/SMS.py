###
# Emin Bugra Saral
# http://www.eminbugrasaral.com/
# version: 0.8
# 2014
#
# Using the API of http://www.solutions4mobiles.com for SMS Messaging
# Please contact http://www.solutions4mobiles.com to use their paid services 
#
# NOTE: This Python class is written by using examples from
# http://www.solutions4mobiles.com/en/developer-network/apis.html
#
# LICENSE:																																	|
# Distributed under the General Public License v3 (GPLv3)										|
# http://www.gnu.org/licenses/gpl-3.0.html																	|
# This program is distributed AS IS and in the hope that it will be useful	|
# WITHOUT ANY WARRANTY; without even the implied warranty of								|
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.      
###

import requests
import urllib
import urlparse

class SMS:
	# Naming with rescect to urlparse library
	scheme = 'http://'
	hostname = 'solutions4mobiles.com'
	
	send_path = '/bulksms/bulksend.go'
	balance_path = '/bulksms/getBALANCE.go'

	# Request url
	send_url = scheme + hostname + send_path
	balance_url = scheme + hostname + balance_path

	# Please visit this page for the explanations of parameters:
	# http://www.solutions4mobiles.com/downloads/documents/SMS_HTTP_API_V%7C7.7%7C.pdf
	default_params = {
		'username': 'username',
		'password': 'password',
		'provider': 'solutions4mobiles.com',
		'msgtext': 'Hello World',
		'originator': 'TestAccount',
		'phone': '901231231212',
		'showDLR': 0,
		'charset': 0,
		'msgtype': '',

	}

	def __init__(self, **kwargs):
		"""
		Update (replace) default params dictionary with given arguments
		An additional parameter is 'hostname', e.g: 192.168.1.2 or www.myhost.com
		Note: IPADDRESS (hostname), username and password are
		provided to users by their Account Managers by email.
		"""
		if kwargs:
			for key, value in kwargs.items():
				if key == 'hostname':
					self.__refresh_url(new_hostname=value)
				elif key in self.default_params:
					self.default_params[key] = value

		# Create attributes from the keys of params dictionary
		self.__populate_attributes()

	def __refresh_url(self, new_hostname=None):
		if new_hostname:
			url = urlparse.urlparse(new_hostname)
			if url.netloc:
				new_url = url.netloc + url.path
			else:
				new_url = url.path

			self.hostname = new_url

		self.send_url = '%s%s%s' % (self.scheme, self.hostname, self.send_path)
		self.balance_url = '%s%s%s' % (self.scheme, self.hostname, self.balance_path)

	def __populate_attributes(self):
		for key, value in self.default_params.items():
			setattr(self, key, value)

	def __update_attributes(self):
		for key, value in self.default_params.items():
			if key in self.__dict__:
				try:
					self.default_params[key] = getattr(self, key)
				except:
					continue

	# Returns:
    	# OK		Successfully Sent
    	# ERROR100	Temporary Internal Server Error. Try again later
    		# ERROR101	Authentication Error (Not valid login Information)
    		# ERROR102	No credits available
    		# ERROR103	MSIDSN (phone parameter) is invalid or prefix is not supported
    		# ERROR104	Tariff Error
    		# ERROR105	You are not allowed to send to that destination/country
    		# ERROR106	Not Valid Route number or you are not allowed to use this route
    		# ERROR107	No proper Authentication (IP restriction is activated)
    		# ERROR108	You have no permission to send messages through HTTP API
    		# ERROR109	Not Valid Originator
    		# ERROR999	Invalid HTTP Request
    	# if showDLR is set to 1 a unique id for the delivery report of this SMS is returned with the OK return value.
    # 
	def send(self, text=False):
		"""
		You have to set text as True if you would like to get
		errors listed above, otherwise you will get a request object
		"""
		self.__refresh_url()
		self.__update_attributes()

		request = requests.get(self.send_url, params=self.default_params)
		if text:
			return request.text
		else:
			return request
