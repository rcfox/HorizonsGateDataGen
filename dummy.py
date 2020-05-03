from boatlib.data import (
    Action,
    ActionAOE,
    ActorPrefab,
    ActorType,
    ActorTypeReaction,
    AvAffecter,
    AvAffecterAOE,
    DialogNode,
    DialogOption,
    Duration,
    FURNACE_IDS,
    ItemReaction,
    ItemType,
    collect_records,
)

def define_dummy():
    with collect_records() as c:
        ActorPrefab('dehydrated_dummy',
                    name='Dummy',
                    skinPalette='pOrange',
                    armorPalette='pOrange',
                    unarmoredPalette='pOrange',
                    clothPalette='pOrange',
                    playerCanOpenInv=True,
                    unkillable=True,
                    hostile=False,
                    faction='player',
                    actorTypeID=ActorType('dehydrated_dummy',
                                          cloneFrom='dummy',
                                          reactions=[
                                              ActorTypeReaction(element=['dispel', 'combatStart'],
                                                                spawnItem='dehydrated_dummy_placeable',
                                                                action=Action('dispel_dehydrated_dummy',
                                                                              av_affecters=[
                                                                                  AvAffecter(actorValue='removeActor',
                                                                                             magnitude=1)
                                                                              ])),
                                          ])
        )

        item = ItemType('dehydrated_dummy_placeable',
                        name='Dehydrated Dummy',
                        description='Place it on the ground and add water.',
                        sprite=26,
                        pR='pOrange',
                        itemCategory='tool',
                        weight=1,
                        volume=10,
                        value=1000,
                        reactions=[
                            ItemReaction(element='water',
                                         newID='X',
                                         action=Action('spawn_dummy',
                                                       special='cantUseInCombat',
                                                       av_affecters=[
                                                           AvAffecter(actorValue='summonActor',
                                                                      magnitude='dehydrated_dummy',
                                                                      chance=100,
                                                                      duration=Duration.permanent()),
                                                       ]))
                        ])

        add_dialog(item)
        return c

def add_dialog(item):
    buy_node = DialogNode('port6_dojo_buy_dummy',
                          statements=[
                              'How would you like to buy this dehydrated training dummy?',
                              'Just place the seed on the ground and add water!',
                              'You can even dispel it when you want to pack it back up.',
                          ])
    buy_node.add_option('Yes ($1,000)',
                        DialogNode('port6_dojo_buy_dummy_yes',
                                   statements=[
                                       ('happy', 'Here you go!')
                                   ],
                                   specialEffect=[
                                       'subtract1000gp',
                                       f'giveItem,{item.id},1',
                                   ],
                                   nextNodeID=''),
                        formulaReq='m:money - 999')
    buy_node.add_option('<color=SlateGray>Can\'t afford it...',
                        'previous',
                        formulaReq='1000 - m:money')
    buy_node.add_option('No', 'previous', newLineOfOptions=True)


    train_node = DialogNode('port6_dojo3',
                            statements=['Hey there <pname=>.<p> Are you here to train?'])
    train_node.add_option('Hammer Skill<adjX=3><iconBig=skill_Hammer> Training', 'port6_dojo3_train',
                          formulaReq='1-g:skill_Hammer_bonus')
    train_node.add_option('Buy a training dummy', buy_node, newLineOfOptions=True)
    train_node.add_option('Goodbye', '', bottomOption=True)

    finished_node = DialogNode('port6_dojo4',
                               statements=[
                                   ('sly', '''Hey <pname=>.<p> How's our training working for you?'''),
                                   ('happy', '''Come back whenever.<p> I'd hate for you to forget how to hold a hammer.''')
                               ])
    finished_node.add_option('Buy a training dummy', buy_node)
    finished_node.add_option('Goodbye', '', bottomOption=True)

if __name__ == '__main__':
    print(define_dummy().serialize())
