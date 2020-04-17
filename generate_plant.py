'''
[ItemType]
name=Aldleaf Seeds;
ID=aldleafSeeds;
sprite=483;
itemCategory=plant;
spriteWhenHeld=0;
description=Small, bristly seeds.;
pR=overworld1;
pG=pOrange;
value=2;
special=canAlwaysFitInTileWhenSpawned;
weight=0;
volume=1;
value=5;
stackable=false;
[ItemReaction]
ID=aldleafSeeds;
element=growth;
newID=aldleafPlant;
[ItemReaction]
ID=aldleafSeeds;
element=water;
newID=aldleafSeeds_watered;


'''

import networkx as nx
from networkx.drawing.nx_pydot import write_dot as _write_dot

class Serialize:
    def __init__(self, id, properties, sub_types):
        self.id = id
        self.properties = properties
        self.sub_types = sub_types

    def serialize(self):
        return self._serialize(self)

    def _serialize(self, owner):
        strings = [f'[{self.__class__.__name__}] ID={owner.id};']
        for key, value in self.properties.items():
            if isinstance(value, list):
                for v in value:
                    strings.append(f'{key}={v};')
            else:
                strings.append(f'{key}={value};')
        for sub_type in self.sub_types:
            strings.append(sub_type._serialize(self))
        return '\n'.join(strings)


class ItemReaction(Serialize):
    def __init__(self, element, newID=None, action=None, spawnItem=None):
        self.element = element
        properties = {}
        if newID:
            properties['newID'] = newID
        if action:
            properties['action'] = action
        if spawnItem:
            properties['spawnItem'] = spawnItem
        super().__init__(None, properties, [])


class ItemType(Serialize):
    def __init__(self, item_id, properties, reactions=None):
        if reactions is None:
            reactions = []
        super().__init__(item_id, properties, reactions)

class Plant:
    def __init__(self, lifecycle):
        self.lifecycle = lifecycle

def define_aldleaf_plant():
    G = nx.MultiDiGraph()
    G.add_edge('seeds', 'seeds_watered', element='wet')
    G.add_edge('seeds_watered', 'sprout', element='newDay')
    G.add_edge('seeds', 'sprout', element='growth')
    G.add_edge('sprout', 'plant', element='newDay', count=3, element_targets={'growth': 'plant_deadend'})
    G.add_edge('plant', 'plant_watered', element='wet')
    G.add_edge('plant_watered', 'bush', element='newDay', count=7)
    G.add_edge('bush', 'bush_watered', element='wet')
    G.add_edge('bush_watered', 'bush', element='newDay', count=7, spawnItem='fruit')

    G.add_edge('plant', 'plant_withered', element='newDay', count=7,
               element_targets={'wet': 'plant_watered', 'growth': 'plant'})
    G.add_edge('bush', 'bush_withered', element='newDay', count=7,
               element_targets={'wet': 'bush_watered'})

    G.add_edge('plant_withered', 'plant', element='growth')
    G.add_edge('bush_withered', 'bush', element='growth')
    return expand_graph(G)

def expand_graph(G):
    to_remove = []
    to_add = []
    for e in G.edges:
        edge = G.edges[e]
        if edge['element'] == 'newDay':
            if 'count' not in edge:
                continue
            element_targets = edge.get('element_targets', {})
            to_remove.append(e)
            head, tail, _ = e
            first = head

            for _ in range(1, edge['count']):
                last = first + '_'
                to_add.append({'__first__': first, '__last__': last, 'element': 'newDay'})
                first = last

                for element, target in element_targets.items():
                    to_add.append({'__first__': first, '__last__': target, 'element': element})

            to_add.append({'__first__': first, '__last__': tail, 'element': 'newDay'})

    for e in to_remove:
        G.remove_edge(*e)

    for e in to_add:
        first = e.pop('__first__')
        last = e.pop('__last__')
        G.add_edge(first, last, **e)

    return G

def write_dot(G, filename):
    for e in G.edges:
        edge = G.edges[e]
        edge['label'] = edge.pop('element')
    return _write_dot(G, filename)

if __name__ == '__main__':
    reactions = [ItemReaction('fire', action='die')]
    i = ItemType('foo', {'bar': 'baz', 'special': ['a', 'b', 'c']}, reactions=reactions)

    define_aldleaf_plant()

    print(i.serialize())
