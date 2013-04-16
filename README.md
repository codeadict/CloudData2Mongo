CloudData2Mongo
===============

Scripts to collect data from OpenStack and CloudStack and stores in MongoDB

To use it first u must install CloudStack python client and Python MongoDB biddings(pymongo):


```bash
$ git clone git://github.com/jasonhancock/cloudstack-python-client.git

$ cd cloudstack-python-client

$ sudo python setup.py install

$ sudo pip install pymongo
```

Then setup Cloud and MongoDB connection settings on *cloud.conf* file
