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
import os, sys, time
import ConfigParser
import httplib, urllib
from urlparse import urlparse
import pymongo
try:
    import simplejson as json
except ImportError:
    import json

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
        """
        initialize Class objects
        """
        self.apitoken = None
        self.apiurl =None
        self.apiurlt = None
        #initialize params for MongoDB
        self.mongo = pymongo.MongoClient(settings.get('MONGODB', 'MONGODB_SERVER'), settings.getint('MONGODB', 'MONGODB_PORT'))
        print self.mongo.alive()
        self.db = self.mongo[settings.get('MONGODB', 'MONGODB_DB')]
        #collection to store the data
        self.collection = self.db['openstack']

    def http_connect(self, url):
        #detect if secure connection is used
        if (settings.getboolean('OPENSTACK', 'HTTPS') == True):
            conn = httplib.HTTPSConnection(url, key_file=path('certs/priv.pem'), cert_file=path('certs/srv_test.crt'))
        else:
            conn = httplib.HTTPConnection(url)
        return conn


    def list_vms(self):
        """
        List all Virtual Machines Available on OpenStack instance.
        """
        params = '{auth{"passwordCredentials":{"username":%s, "password":%s}, "tenantId":"%s"}}' % (settings.get('OPENSTACK', 'USER'), settings.get('OPENSTACK', 'PASS'), settings.get('OPENSTACK', 'TENANT_ID'))
        headers = {"Content-Type": "application/json"}
        initial_url = settings.get('OPENSTACK', 'URL')
        conn = self.http_connect(initial_url)
        print conn
        #Get auth credentials
        conn.request("POST", "/v2.0/tokens", params, headers)
        response = conn.getresponse()
        data = response.read()
        dd1 = json.loads(data)
        #close connection
        conn.close()
        #get the desired Data
        self.apitoken = dd1['auth']['token']['id']
        self.apiurl = dd1['auth']['serviceCatalog']['nova'][0]['publicURL']
        self.apiurlt = urlparse(dd1['auth']['serviceCatalog']['nova'][0]['publicURL'])
        print self.apitoken

        #Get list of servers
        url_srvr_list  = self.apiurlt
        params = urllib.urlencode({})
        headers = { "X-Auth-Token":self.apitoken, "Content-type":"application/json" }
        #make connection
        conn = self.http_connect(url_srvr_list)
        conn.request("GET", "%s/servers/detail" % (self.apiurlt[2]), params, headers)
        response = conn.getresponse()
        data = response.read()
        #return JSON with list of servers
        srvr_list = json.loads(data)
        #close the connection
        conn.close()
        result = []
        #iterate over servers and return only active ones
        for vm in srvr_list['servers']:
            if vm['status'] == 'ACTIVE':
                result.append(vm)
        return result

    def store_data(self, vm):
        """
        Store the data for specific Virtual Machine on MongoDB.
        """
        params = urllib.urlencode({})
        headers = { "X-Auth-Token":self.apitoken, "Content-type":"application/json" }
        #make connection
        conn = self.http_connect(self.apiurlt)
        conn.request("GET", "%s/servers/%s/diagnostics" % (self.apiurlt[2], vm['id']), params, headers)
        #Get the server data response
        response = conn.getresponse()
        data = response.read()
        #return JSON with diagnostic about server
        srvr_info = dict(json.loads(data))
        #add VM id and name to diagnostic dict
        srvr_info["server_id"] = vm['id']
        srvr_info["server_id"] = vm['name']
        inserted_id = self.collection.insert(dict(vm))
        return inserted_id

#Main program
if __name__ == '__main__':
    os = OpenStack()
    for vm in os.list_vms():
        inserted_id = os.collect_data(vm)
        print 'Inserted record on MongoDB with id %s' % inserted_id
        time.sleep(10)
    #Disconnect MongoDB
    os.mongo.disconnect()
    sys.exit()
