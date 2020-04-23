import networkx
from networkx.drawing.nx_pydot import write_dot as _write_dot
from boatlib.data import ItemType, ItemReaction, Collection

def define_aldleaf_plant():
    G = networkx.MultiDiGraph()
    G.add_edge('aldleaf', 'aldleafSeeds', element='smash')
    G.add_edge('aldleafSeeds', 'aldleafSeeds_watered', element='water')
    G.add_edge('aldleafSeeds_watered', 'aldleafSprout', element='newDay')
    G.add_edge('aldleafSeeds', 'aldleafSprout', element='growth')
    G.add_edge('aldleafSprout', 'aldleafPlant_deadend', element='growth')
    G.add_edge('aldleafSprout', 'aldleafPlant', element='newDay', count=3,
               description='It will develop leaves in {x} day{s}.',
               element_targets={'growth': 'aldleafPlant_deadend'})

    G.add_edge('aldleafPlant', 'aldleafPlant_watered', element='water')
    G.add_edge('aldleafPlant_watered', 'aldleafBush', element='newDay', count=7,
               description='It will mature in {x} day{s}.',
               element_targets={'slash': 'aldleaf'})

    G.add_edge('aldleafBush', 'aldleafBush_watered', element='water')
    G.add_edge('aldleafBush_watered', 'aldleafBush', element='newDay', count=7,
               description='It will produce fruit in {x} day{s}.',
               spawnItem='sleep_fruit', element_targets={'slash': 'aldleafPlant'})

    G.add_edge('aldleafPlant', 'aldleafPlant_wither', element='newDay', count=7,
               element_targets={'water': 'aldleafPlant_watered', 'growth': 'aldleafPlant', 'slash': 'aldleaf'})
    G.add_edge('aldleafBush', 'aldleafBush_wither', element='newDay', count=7,
               element_targets={'water': 'aldleafBush_watered', 'slash': 'aldleafPlant', 'growth': 'aldleafBush'})

    G.add_edge('aldleafPlant_wither', 'aldleafPlant', element='growth')
    G.add_edge('aldleafBush_wither', 'aldleafBush', element='growth')

    G.add_edge('aldleafPlant_wither', 'aldleaf', element='slash')
    G.add_edge('aldleafBush_wither', 'aldleafPlant_wither', element='slash')

    G.add_edge('aldleafSprout', 'X', element='slash')
    G.add_edge('aldleafPlant', 'aldleaf', element='slash')
    G.add_edge('aldleafPlant_deadend', 'aldleaf', element='slash')

    G.nodes['aldleaf']['properties'] = dict(
        cloneFrom='aldleaf'
    )
    G.nodes['aldleafSeeds']['properties'] = dict(
        name='Aldleaf Seeds',
        itemCategory='plant',
        sprite=483,
        description='Seeds!'
    )
    G.nodes['aldleafSeeds_watered']['properties'] = dict(
        name='Aldleaf Seeds (Watered)',
        itemCategory='hide',
        cloneFrom='aldleafSeeds',
        special=['dontCloneReactions', 'cannotBePickedUp']
    )
    G.nodes['aldleafSprout']['properties'] = dict(
        name='Aldleaf Sprout',
        itemCategory='plant',
        sprite=556,
        description='It will develop leaves in 3 day.',
        special='cannotBePickedUp'
    )
    G.nodes['aldleafPlant']['properties'] = dict(
        cloneFrom='aldleafPlant',
        special='dontCloneReactions',
        description='It will mature in 7 days if watered.',
    )
    G.nodes['aldleafPlant_deadend']['properties'] = dict(
        cloneFrom='aldleafPlant',
        special='dontCloneReactions'
    )
    G.nodes['aldleafPlant_wither']['properties'] = dict(
        cloneFrom='aldleafPlant_wither',
        special='dontCloneReactions'
    )
    G.nodes['aldleafPlant_watered']['properties'] = dict(
        name='Aldleaf Plant (Watered)',
        itemCategory='hide',
        cloneFrom='aldleafPlant',
        special='dontCloneReactions',
        description='It will mature in 7 days.',
    )
    G.nodes['aldleafBush']['properties'] = dict(
        cloneFrom='aldleafBush',
        special='dontCloneReactions',
        description='It will produce fruit in 7 days if watered.',
    )
    G.nodes['aldleafBush_wither']['properties'] = dict(
        cloneFrom='aldleafBush_wither',
        special='dontCloneReactions'
    )
    G.nodes['aldleafBush_watered']['properties'] = dict(
        name='Aldleaf Bush (Watered)',
        itemCategory='hide',
        cloneFrom='aldleafBush',
        special='dontCloneReactions',
        description='It will produce fruit in 7 days.',
    )

    return graph_to_plants(expand_graph(G))

def expand_graph(G):
    to_remove = []
    to_add = []
    nodes = []
    for e in G.edges:
        edge = G.edges[e]
        if edge['element'] == 'newDay':
            if 'count' not in edge:
                continue
            element_targets = edge.get('element_targets', {})
            to_remove.append(e)
            head, tail, _ = e
            first = head

            for x in range(1, edge['count']):
                last = first + '_'
                properties = {
                    'cloneFrom': first,
                    'special': 'dontCloneReactions',
                    'itemCategory': 'hide'
                }
                if 'description' in edge:
                    days = edge['count'] - x
                    s = 's' if days != 1 else ''
                    properties['description'] = edge['description'].format(x=days, s=s)
                nodes.append((last, properties))
                to_add.append({'__first__': first, '__last__': last, 'element': 'newDay'})
                first = last

                for element, target in element_targets.items():
                    to_add.append({'__first__': first, '__last__': target, 'element': element})

            to_add.append({'__first__': first, '__last__': tail, 'element': 'newDay'})
            spawnItem = edge.get('spawnItem', None)
            if spawnItem:
                to_add[-1]['spawnItem'] = spawnItem

    for e in to_remove:
        G.remove_edge(*e)

    for e in to_add:
        first = e.pop('__first__')
        last = e.pop('__last__')
        G.add_edge(first, last, **e)

    for n, p in nodes:
        G.nodes[n]['properties'] = p

    return G

def graph_to_plants(G):
    items = []
    for node in G:
        if node == 'X':
            continue

        reactions = []
        for tail in G[node]:
            edge = G[node][tail][0]
            element = edge['element']
            spawnItem = edge.get('spawnItem', None)
            action = edge.get('action', None)
            r = ItemReaction(element, newID=tail, spawnItem=spawnItem, action=action)
            reactions.append(r)
        i = ItemType(node, reactions=reactions, **G.nodes[node].get('properties', {}))
        items.append(i)

    return Collection(*items)


def write_dot(G, filename):
    for e in G.edges:
        edge = G.edges[e]
        edge['label'] = edge.pop('element')
    return _write_dot(G, filename)

if __name__ == '__main__':
    print(define_aldleaf_plant().serialize())
