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
import ConfigParser
import httplib
import pymongo

settings = ConfigParser.ConfigParser()
settings.read('cloud.conf')

class OpenStack(object):
    '''
    Class to gather data from OpenStack Virtual Machines
    '''
    def collect_data(self):
        params = '{auth{"passwordCredentials":{"username":%s, "password": %s}}}' %(settings.get('MONGODB', 'MONGODB_SERVER'), settings.get('MONGODB', 'MONGODB_SERVER')
        #dettect if secure connection is used
        if (settings.getboolean('OPENSTACK', 'HTTPS') == True):
            conn = httplib.HTTPSConnection(url, key_file='../cert/priv.pem', cert_file='../cert/srv_test.crt')
        else:
            conn = httplib.HTTPConnection(url)

    def mongo_it(self):
        pass


