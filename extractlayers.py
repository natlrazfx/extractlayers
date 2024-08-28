# Natalia Raz

import nuke


def createLayerShuffles(node):
    channels = node.channels()
    print("Available channels:", channels)  # Available channels list
    layers = list(set([c.split('.')[0] for c in channels]))

    for layer in layers:
        shuffleNode = nuke.createNode('Shuffle2', inpanel=False)
        shuffleNode.setInput(0, node)
        shuffleNode['in1'].setValue(layer)
        shuffleNode['out1'].setValue('rgba')
        shuffleNode['label'].setValue(layer)
        shuffleNode['postage_stamp'].setValue(True)

        if layer == 'depth' and 'depth.Z' in channels:
            # depth issue solution
            mappings = [
                ('depth.Z', 'rgba.red'),
                ('depth.Z', 'rgba.green'),
                ('depth.Z', 'rgba.blue'),
                ('depth.Z', 'rgba.alpha')
            ]
            shuffleNode['mappings'].setValue(mappings)
        else:
            # other layers
            shuffleNode['in1'].setValue(layer)

        removeNode = nuke.createNode('Remove', inpanel=False)
        removeNode.setInput(0, shuffleNode)
        removeNode['operation'].setValue('keep')
        removeNode['channels'].setValue('rgba')


# run selected
selected_node = nuke.selectedNode()
createLayerShuffles(selected_node)
