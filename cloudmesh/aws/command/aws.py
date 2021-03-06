from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.api.aws_client import Aws
import os
from cloudmesh.common.ConfigDict import ConfigDict
from cloudmesh.common.StopWatch import StopWatch
from cloudmesh.common.default import Default

from cloudmesh.common.StopWatch import StopWatch
#Console printing packages
from cloudmesh.common.console import Console

class AwsCommand(PluginCommand):

    @command
    def do_aws(self, args, arguments):
        """
        ::

          Usage:
            aws refresh ON
            aws api URL
            aws default image ON
            aws image [refresh] [--format=FORMAT]
            aws image list [--format=FORMAT]
            aws flavor [refresh] [--format=FORMAT]
            aws flavor list [--format=FORMAT]
            aws vm boot NODE_NAME [--image_id=IMAGE_ID] [--flavor_id=FLAVOR_ID] [--keypair_name=KEYPAIR_NAME]
            aws vm reboot NODE_NAME
            aws vm delete NODE_NAME
            aws vm list [--format=FORMAT]
            aws vm refresh [--format=FORMAT]
            aws keypair create NAME
            aws keypair delete NAME
            aws keypair list
            aws keypair refresh
            aws keypair get NAME
            aws location list
            aws location refresh
            aws volume create VOLUME_NAME
            aws volume list
            aws volume refresh
            aws volume delete VOLUME_NAME
            aws volume attach VOLUME_NAME
            aws drop collections

          Arguments:
            ON              set configuration to on/off 
            NAME            The name of the aws
            URL             URL of aws API
            FORMAT          The format in which to print the data
            UUID            Unique User ID, which gets generate after creating the node/vm
            IMAGE_ID        Image ID for which we are creating the vm
            KEYPAIR_NAME    Created Key pair name
            FLAVOR_ID       Flavor ID for which vm request to be establish
            VOLUME_ID       Unique ID after creating a volume
          Options:
            -v       verbose mode

          Description:
            Manages a virtual aws on a cloud

            to complete the command see the man page of cm boot help
        """
        v = Default()
        if v['aws', 'refresh'] != None:
            refresh = v['aws', 'refresh']
        else:
            refresh = "off"
        v.close()
       
   
        if arguments.refresh and arguments.ON:
            v = Default()
            v['aws', 'refresh'] = arguments.ON
            v.close()

        """ v = Default()
        if v['aws', 'keypair'] != None:
            print("assign the name")
            NAME = v['aws', 'keypair']
        v.close()"""
        
        """if arguments.create and arguments.NAME :
           print(" create new obj :: ",arguments.NAME )
           v = Default()
           v['aws', 'keypair'] = arguments.NAME
           v.close()"""
   
        # Initialize timer and aws client 
        stopwatch = StopWatch()
        stopwatch.start('E2E')
        aws = Aws()

        if arguments.image: 
            if arguments.refresh or refresh == "on":
                aws.image_refresh()
            else:
                aws.image_list()

            stopwatch.stop('E2E')
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            return

        if arguments.flavor: 
            if arguments.refresh or refresh == "on":
                aws.flavor_refresh()
            else:
                aws.flavor_list()

            stopwatch.stop('E2E')
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            return

        if arguments.vm and arguments.list :
            aws.node_list()
            stopwatch.stop('E2E')
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            return

        if arguments.vm and arguments.refresh :
            aws.node_refresh(True)
            stopwatch.stop('E2E')
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            return

        if arguments.vm and arguments.reboot and arguments.NODE_NAME :
            NODE_NAME = arguments.NODE_NAME
            aws.node_reboot(NODE_NAME)
            stopwatch.stop('E2E')
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            

        if arguments.vm and arguments.boot and arguments.NODE_NAME :
            #SEL_IMAGE_ID = 'ami-0183d861' #ami-d85e75b0
            arguments.IMAGE_ID = arguments["--image_id"]
            arguments.FLAVOR_ID = arguments["--flavor_id"]
            arguments.KEYPAIR_NAME = arguments["--keypair_name"]
            config = {}
            if arguments.IMAGE_ID:
                config["image_id"] = arguments.IMAGE_ID
            
            if arguments.FLAVOR_ID:
                config["flavor_id"] = arguments.FLAVOR_ID

            if arguments.KEYPAIR_NAME:
                config["keypair_name"] = arguments.KEYPAIR_NAME

            # if arguments.SEC_GRP_NAMES:
            #     config["security_group_names"] = arguments.SEC_GRP_NAMES

            

           
            aws.node_create_by_imageId(arguments.NODE_NAME,config)
            stopwatch.stop('E2E')
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            return
 
        if arguments.vm and arguments.delete and arguments.NODE_NAME:
            node_name =  arguments.NAME #'61671593de3681e7de6bd6c6e33f5a4857110864'
            aws.node_delete(node_name)
            stopwatch.stop('E2E')
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            return
        
        if arguments.keypair and arguments.create and arguments.NAME:
            KEY_PAIR = arguments.NAME #"AWS3"
            aws.keypair_create(KEY_PAIR)
            stopwatch.stop('E2E')
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            return

        if arguments.keypair and arguments.delete and arguments.NAME:
            KEY_PAIR = arguments.NAME # "AWS1"
            aws.keypair_delete(KEY_PAIR)
            stopwatch.stop('E2E')
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            return

        if arguments.keypair and arguments.list :
            aws.keypair_list()
            stopwatch.stop('E2E')
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            return

        if arguments.keypair and arguments.refresh :
            aws.keypair_refresh()
            stopwatch.stop('E2E')
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            return
        
        if arguments.keypair and arguments.get and arguments.NAME :
            KEY_PAIR =  arguments.NAME #"AWS2"
            aws.keypair_get(KEY_PAIR)
            stopwatch.stop('E2E')
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            return
            
        if arguments.drop and arguments.collections :
            aws.drop_collections()
            stopwatch.stop('E2E')
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            return
        
        if arguments.location and arguments.list:
            aws.location_list(True)
            stopwatch.stop('E2E')
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            return

        if arguments.location and arguments.refresh:
            aws.location_refresh(True)
            stopwatch.stop('E2E')
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            return
          
        if arguments.volume and arguments.create and arguments.VOLUME_NAME:
            VOLUME_SIZE = 1 # Size of volume in gigabytes (required)
            VOLUME_NAME =  arguments.VOLUME_NAME # Name of the volume to be created
            aws.volume_create(VOLUME_SIZE,VOLUME_NAME)
            stopwatch.stop('E2E')
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            return
        
        if arguments.volume and arguments.list:
            aws.volume_list(True)
            stopwatch.stop('E2E')
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            return

        if arguments.volume and arguments.refresh:
            aws.volume_refresh(True)
            stopwatch.stop('E2E')
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            return

        if arguments.volume and arguments.delete and arguments.VOLUME_NAME :
            aws.volume_delete(arguments.VOLUME_NAME)
            stopwatch.stop('E2E')
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            return
        
        if arguments.volume and arguments.attach and arguments.VOLUME_ID :
            NODE_ID = '' # we are taking defaulr 0th created node from node list
            aws.volume_attach(NODE_ID, arguments.VOLUME_ID)
            stopwatch.stop('E2E')
            Console.ok('Execution Time:' + str(stopwatch.get('E2E')))
            return
