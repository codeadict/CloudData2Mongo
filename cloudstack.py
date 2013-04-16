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
import ConfigParser, logging
from urllib2 import URLError
import CloudStack
import pymongo

settings = ConfigParser.ConfigParser()
settings.read('cloud.conf')

class CSClient(object):
    def init(self):
        #MongoDB connection
        self.mongo = pymongo.Connection(settings.get('MONGODB', 'MONGODB_SERVER'), settings.get('MONGODB', 'MONGODB_PORT'))
        self.db = mongo(settings.get('MONGODB', 'MONGODB_DB'))
        #collection to store the data
        self.collection = self.db['cloudstack']

    def store_data(self):
        #init CloudStack Client
        try:
            cs = CloudStack.Client(settings.get('CLOUDSTACK', 'API'), settings.get('CLOUDSTACK', 'APIKEY'), settings.get('CLOUDSTACK', 'SECRET'))
            vms = cs.listVirtualMachines()
            #iterate over each Virtual Machine and push data to mongo DB
            for vm in vms:
                print vm['name']
                inserted_id = self.collection.insert(dict(vm))
                print 'Inserted record on MongoDB with id %s' % inserted_id
        except URLError:
            print 'Error connecting to CloudStack instance. I think connection params are wrong :('
        except:
            print 'An undeterminable error has ocurred'

client = CSClient()
client.store_data()

