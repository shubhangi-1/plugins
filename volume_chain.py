#!/usr/bin/python

#
# Author: Ankit Agarwal (ankit.jsr167@gmail.com)
# Created: 23 Nov, 2016
# Last modified: 05 Jun, 2017
#
# The script displays a tree of dependencies between volumes and snapshots in
# Openstack. A volume may have dependent snapshots, which further may have
# dependent volumes and so on. This script would help in resolving the problem,
# by listing the chain of dependencies.
#

from keystoneclient.auth.identity.v3 import Password
from keystoneclient import session
from keystoneclient import client as kclient
from keystoneclient.v3 import client as keystoneclient
from novaclient.v2 import client as novaclient
from cinderclient.v1 import client as cinderclient

from Queue import Queue
import argparse
import sys


def get_session():
    # Get authentication
    auth = Password(auth_url="http://controller:5000/v3",
                    password="<Password>".replace("$$", "$"),
                    username="<username>",
                    user_domain_id="default",
                    project_name="<project name>",
                    project_domain_id="default")

    # Get session
    sess = session.Session(auth=auth)
    return sess


class Node:
    def __init__(self, ID, Name, Type):
        self.ID = ID
        self.Name = Name
        self.Type = Type
        self.dependency = []


class VolumeTree:
    root = None

    #
    # Build the dependency tree of volumes and snapshots.
    # Note: The root node of the tree would always be a volume.
    #
    def buildTree(self, root, ID, Name, Type, cinder_client):
        if root is None:
            root = Node(ID, Name, Type)
        if root.Type == 'Volume':
            volume = cinder_client.volumes.get(root.ID)
            # Gathering snapshot list created from the above volume.
            snapshot_list = getattr(volume, 'snapshots_list')
            # Adding snapshot list elements to the tree.
            for snapshot_id in snapshot_list:
                snapshot = cinder_client.volume_snapshots.get(snapshot_id)
                snapshot_name = getattr(snapshot, 'name')
                root.dependency.append(Node(snapshot_id, snapshot_name,
                                       'Snapshot'))
        elif root.Type == 'Snapshot':
            snapshot = cinder_client.volume_snapshots.get(root.ID)
            # Gathering volume list created from the above snapshot.
            volume_list = getattr(snapshot, 'volumes_created')
            # Adding volume list elements to the tree.
            for volume_id in volume_list:
                volume = cinder_client.volumes.get(volume_id)
                volume_name = getattr(volume, 'name')
                root.dependency.append(Node(volume_id, volume_name, 'Volume'))
        # Recursively building the tree.
        for value in root.dependency:
            self.buildTree(value, value.ID, value.Name, value.Type,
                           cinder_client)
        return root

    #
    # Display the dependencies starting from the source volume as the root.
    #
    def displayTree(self, root):
        q = Queue()
        q.put(root)
        while q.empty() is False:
            temp = q.get()
            print "%s (%s) --->" % (temp.Name, temp.ID),
            if len(temp.dependency) == 0:
                print 'NULL'
                continue
            for value in temp.dependency:
                print "%s (%s)" % (value.Name, value.ID),
                q.put(value)
            print


#
# Accept source volume id from the user. Build the tree.
# Display the dependencies.
#
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("volume_id", help="enter volume id")
    args = parser.parse_args()
    sess = get_session()
    cc = cinderclient.Client(session=sess)
    vol_tree = VolumeTree()
    #
    # Exception handled if there is no volume present with the entered id.
    #
    try:
        source_volume = cc.volumes.get(args.volume_id)
    except Exception:
        print "Volume ID not found"
        return 2
    source_volume_name = getattr(source_volume, 'name')
    vol_tree.root = vol_tree.buildTree(vol_tree.root, args.volume_id,
                                       source_volume_name, 'Volume', cc)
    vol_tree.displayTree(vol_tree.root)

if __name__ == '__main__':
    sys.exit(main())
