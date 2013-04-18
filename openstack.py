#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 Dairon Medina <dairon.medina@gmail.com>. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import ConfigParser
import httplib
import pymongo

settings = ConfigParser.ConfigParser()
settings.read('cloud.conf')

#take relative path to this folder
ROOT = os.path.dirname(os.path.abspath(__file__))
path = lambda *a: os.path.join(ROOT, *a)

class OpenStack(object):
    '''
    Class to gather data from OpenStack Virtual Machines
    '''
    def __init__(self):
        #initialize params to MongoDB
        self.mongo = pymongo.Connection(settings.get('MONGODB', 'MONGODB_SERVER'), settings.getint('MONGODB', 'MONGODB_PORT'))
        self.db = self.mongo(settings.get('MONGODB', 'MONGODB_DB'))
        #collection to store the data
        self.collection = self.db['openstack']

    def collect_data(self):
        #params = '{auth{"passwordCredentials":{"username":%s, "password": %s}}}' %(settings.get('MONGODB', 'MONGODB_SERVER'), settings.get('MONGODB', 'MONGODB_SERVER')
        #dettect if secure connection is used
        if (settings.getboolean('OPENSTACK', 'HTTPS') == True):
            conn = httplib.HTTPSConnection(url, key_file=path('certs/priv.pem'), cert_file=path('certs/srv_test.crt'))
        else:
            conn = httplib.HTTPConnection(url)

    def mongo_it(self):
        pass

os = OpenStack()
os.collect_data()


