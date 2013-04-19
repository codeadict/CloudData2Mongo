CloudData2Mongo
===============

Scripts to collect data from OpenStack and CloudStack and stores in MongoDB

Author: Dairon Medina <dairon.medina@gmail.com>

Usage:
----------
To use it first u must install CloudStack python client and Python MongoDB biddings(pymongo):


```bash
$ git clone git://github.com/jasonhancock/cloudstack-python-client.git

$ cd cloudstack-python-client

$ sudo python setup.py install

$ sudo pip install pymongo
```

Then setup Cloud and MongoDB connection settings on *cloud.conf* file

To use Certificates for Secure(HTTPS) connection to OpenStack copy the files *priv.pem* and *srv_test.crt* to certs/ directory and put setting **HTTPS** to False on **OPENSTACK** section; *cloud.conf*  file.