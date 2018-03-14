#!/usr/bin/python
#coding:utf-8

from kazoo.client import KazooClient
from kazoo.client import KazooState,KeeperState
from kazoo.exceptions import NoNodeException,NodeExistsException,KazooException
import logging

log = logging.getLogger(__name__)
class AbstractZookeeperClient(object):
    '''zookeeper basic operation '''
    def __init__(self,servs,logger,timeout,**kwargs):
        self.logger = logger or log
        try:
            self.ZkClient = KazooClient(hosts=servs,timeout=timeout,logger=self.logger,**kwargs)
            self.ZkClient.start()
            self._iszktimeout = False
        except KazooException as why:
            self.logger.error('%s',why)
            self._iszktimeout = True
        self.ZkClient.add_listener(self.state_listener)
        
    def _close(self):
        self.ZkClient.stop()

    @property
    def client(self):
        return self.ZkClient

    @property
    def iszktimeout(self):
        return self._iszktimeout     

    def _is_connected(self):
        return KazooState.CONNECTED

    def state_listener(self,state):
        '''When a connection transitions to LOST, any ephemeral nodes that have been created will be removed by Zookeeper 
            And when to CONNECTED ,need to reinit ephemeral nodes '''
        if state == KazooState.LOST:
            self._iszktimeout = True
            self.logger.error('Zookeeper connection %s',state)
        if state == KazooState.CONNECTED:
            self._iszktimeout = False
            if self.ZkClient.client_state == KeeperState.CONNECTED_RO:
                self.logger.info('Zookeeper connection %s',self.ZkClient.client_state)
            else:
                self.logger.info('Zookeeper connection %s',state)

    def create_path(self,path):
        if path.endswith('/'):
            try:
                self.ZkClient.ensure_path(path)
                self.logger.info('%s path create',path)
            except NodeExistsException as why:
                self.logger.warn("ZkNode exists %s",why)

    def getdata(self,path):
        try:
            data,stat = self.ZkClient.get(path)
        except NoNodeException as why:
            self.logger.warn('%s',why)
            return None
        return data
        
    def get_kvlist_byparent(self,parentPath):
        '''gets a list of the children of a given parent's node return key=Value List
               '''
        KeyList = self.ZkClient.get_children(parentPath)
        return [ key + '=' + self.getdata(parentPath+'/'+key) for key in KeyList ]
        
    def get_kvmap_byparent(self,parentPath):
        ''' gets a dict of the children of a given parent's node return kv dict 
            '''
        KeyList = self.ZkClient.get_children(parentPath)
        KeyValueDict = dict([(key,self.getdata(parentPath+'/'+key)) for key in KeyList])
        return KeyValueDict
        
    def create_node(self,path,value,is_ephemeral=False,is_makepath=True):
        '''Create a node with data return boolean '''
        result = None
        if path.endswith('/'):
            try:
                result = self.ZkClient.create(path,value,ephemeral=is_ephemeral,makepath=is_makepath)
            except KazooException as why:
                self.logger.warn('create node err %s' % why)
                result = False
        return True if result else False



