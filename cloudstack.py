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
import ConfigParser, os
import CloudStack
import pymongo

settings = ConfigParser.ConfigParser()
settings.readfp(open('cloud.conf'))

class CSClient(object):

    def init(self):
        self.cs = CloudStack.Client(api, apikey, secret)

        self.mongo = pymongo.Connection(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])

        self.db = mongo[settings['MONGODB_DB']]

    vms = cs.listVirtualMachines()

    def store_data(self):
        for vm in vms:
            print vm['name']
            self.collection.insert(dict(vm))
