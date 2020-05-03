import uuid
import contextlib
import collections

FURNACE_IDS = ['furnace_lit', 'furnace2_lit', 'furnace_everlit1', 'furnace_everlit2']

__NO_ID__ = object()

def generate_id(prefix):
    return prefix + str(uuid.uuid4()).replace('-', '')

@contextlib.contextmanager
def collect_records():
    c = Collection()
    Serialize.push_collection(c)
    yield c
    Serialize.pop_collection()

class Duration:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError('do not instantiate Duration directly')

    @staticmethod
    def ticks(count):
        if count <= 0:
            raise ValueError('count must be greater than 0')
        return count

    @staticmethod
    def indefinite():
        return -1

    @staticmethod
    def instantaneous():
        return -2

    @staticmethod
    def permanent():
        return -2

    @staticmethod
    def start_of_turn():
        return -3

    @staticmethod
    def end_of_turn(count=1):
        if count < 1:
            raise ValueError('count must be greater than 0')
        return -3 - count

class Serialize:
    _collection_stack = collections.deque([])

    def __init__(self, id, properties, subtypes=None):
        self.id = id
        self.properties = properties

        if subtypes is None:
            subtypes = []
        self.subtypes = subtypes

        if len(self._collection_stack) and id is not None and id is not __NO_ID__:
            self._collection_stack[-1].append(self)

    @classmethod
    def push_collection(cls, c):
        cls._collection_stack.append(c)

    @classmethod
    def pop_collection(cls):
        return cls._collection_stack.pop()

    def serialize(self):
        return self._serialize(self)

    def _str(self, value):
        if isinstance(value, str):
            return value
        elif isinstance(value, bool):
            return str(value).lower()
        elif hasattr(value, 'id'):
            return value.id
        else:
            return str(value)

    def _serialize(self, owner):
        strings = [f'[{self.__class__.__name__}]']
        if self.id is not __NO_ID__:
            strings.append(f'    ID={owner.id};')
        for key, value in self.properties.items():
            if isinstance(value, list):
                for v in value:
                    strings.append(f'    {key}={self._str(v)};')
            else:
                strings.append(f'    {key}={self._str(value)};')
        if self.subtypes:
            for subtype in self.subtypes:
                strings.append(subtype._serialize(owner))
        return '\n'.join(strings)

    def collect(self, collection):
        collection.append(self)
        return self

class Collection:
    def __init__(self, *items):
        self.items = list(items)

        if len(Serialize._collection_stack):
            Serialize._collection_stack[-1].append(self)

    def serialize(self):
        return '\n\n'.join(i.serialize() for i in self.items)

    def append(self, item):
        self.items.append(item)

class ItemReaction(Serialize):
    def __init__(self, **kwargs):
        super().__init__(None, kwargs)

class ItemType(Serialize):
    def __init__(self, item_id, reactions=None, **kwargs):
        properties = dict(kwargs)
        if 'special' in properties:
            if not isinstance(properties['special'], list):
                properties['special'] = [properties['special']]
        super().__init__(item_id, properties, subtypes=reactions)

    def recipe(self, material, result, consume_on_combine=False, reverse_with=None):
        if reverse_with:
            combine_withs = result.properties.get('combineWith', [])
            to_makes = result.properties.get('toMake', [])
            consume_on_combines = result.properties.get('consumeOnCombine', [])

            for r in reverse_with:
                combine_withs.append(r)
                to_makes.append(material)
                consume_on_combines.append(consume_on_combine)

            result.properties['!combineWith'] = ','.join(combine_withs)
            result.properties['!toMake'] = ','.join(to_makes)
            result.properties['!consumeOnCombine'] = ','.join([self._str(x) for x in consume_on_combines])

        return ItemType(material,
                        cloneFrom=material,
                        combineWith=self,
                        toMake=result,
                        consumeOnCombine=consume_on_combine)

class GlobalTrigger(Serialize):
    def __init__(self, alias_id, effects, **kwargs):
        for p in ('topX', 'topY', 'btmX', 'btmY'):
            if p not in kwargs:
                kwargs[p] = 0

        kwargs['aliasID'] = alias_id
        super().__init__(alias_id, kwargs, subtypes=effects)

class GlobalTriggerEffect(Serialize):
    def __init__(self, effect_id, x=None, y=None, delay=None, strings=None, floats=None, bools=None):
        properties = {
            'effectID': effect_id
        }
        if x is not None:
            properties['xValue'] = x
        if y is not None:
            properties['yValue'] = y
        if delay is not None:
            properties['delay'] = delay
        if strings:
            if len(strings) > 0:
                properties['sValue'] = strings[0]
            if len(strings) > 1:
                properties['sValue2'] = strings[1]
        if floats:
            if len(floats) > 0:
                properties['fValue'] = floats[0]
            if len(floats) > 1:
                properties['fValue2'] = floats[1]
        if bools:
            if len(bools) > 0:
                properties['bValue1'] = bools[0]
            if len(bools) > 1:
                properties['bValue2'] = bools[1]

        super().__init__(None, properties)

class Action(Serialize):
    def __init__(self, action_id, aoe=None, av_affecters=None, **kwargs):
        if aoe is None:
            self.aoe = ActionAOE.basic()
        else:
            self.aoe = aoe
        if self.aoe.__class__.__name__ != 'ActionAOE':
            raise ValueError('Action aoe must be of type ActionAOE')

        if isinstance(av_affecters, list):
            self.av_affecters = av_affecters
        else:
            self.av_affecters = [av_affecters]

        subtypes = [self.aoe]
        subtypes.extend(self.av_affecters)

        super().__init__(action_id, kwargs, subtypes=subtypes)


class ActionAOE(Serialize):
    def __init__(self, **kwargs):
        super().__init__(None, kwargs)

    @classmethod
    def basic(cls):
        return cls(cloneFrom='oneTile')

class AvAffecter(Serialize):
    def __init__(self, aoe=None, **kwargs):
        if aoe is None:
            aoe = AvAffecterAOE.basic()
        if aoe.__class__.__name__ != 'AvAffecterAOE':
            raise ValueError('AvAffecter aoe must be of type AvAffecterAOE')
        if 'duration' not in kwargs:
            kwargs['duration'] = Duration.instantaneous()
        super().__init__(None, kwargs, subtypes=[aoe])

class AvAffecterAOE(ActionAOE):
    pass

class DialogNode(Serialize):
    def __init__(self, dialog_id=None, statements=None, **kwargs):
        if dialog_id is None:
            dialog_id = generate_id('dialog_')
        if statements is None:
            statements = []

        animations = []
        lines = []

        for s in statements:
            if isinstance(s, str):
                lines.append(s)
                animations.append('')
            else:
                animation, line = s
                lines.append(line)
                animations.append(animation)

        kwargs['animations'] = animations
        kwargs['statements'] = lines

        super().__init__(dialog_id, kwargs)

    def add_option(self, text, node, **kwargs):
        self.subtypes.append(DialogOption(text, node, **kwargs))
        return self

class DialogOption(Serialize):
    def __init__(self, text, node, **kwargs):
        kwargs['text'] = text
        kwargs['nodeToConnectTo'] = node
        option_id = kwargs.pop('ID', __NO_ID__)
        super().__init__(option_id, kwargs)

class ActorPrefab(Serialize):
    # I think there's more to this, but it's all I need for now.
    def __init__(self, prefab_id, **kwargs):
        super().__init__(prefab_id, kwargs)

class ActorType(Serialize):
    def __init__(self, actor_id, reactions=None, **kwargs):
        properties = dict(kwargs)
        if 'special' in properties:
            if not isinstance(properties['special'], list):
                properties['special'] = [properties['special']]
        super().__init__(actor_id, properties, subtypes=reactions)

class ActorTypeReaction(ItemReaction):
    pass
