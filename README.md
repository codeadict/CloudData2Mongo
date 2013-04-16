CloudData2Mongo
===============

Scripts to collect data from OpenStack and CloudStack and stores in MongoDB

To use it first u must install CloudStack python client:


```bash
$ git clone git://github.com/jasonhancock/cloudstack-python-client.git

$ cd cloudstack-python-client

$ sudo python setup.py install
```

Then setup Cloud and MongoDB connection settings on *cloud.conf* file
