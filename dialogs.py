from boatlib.data import (
    Action,
    ActionAOE,
    ActorPrefab,
    ActorType,
    ActorTypeDetectAoE,
    AvAffecter,
    AvAffecterAOE,
    DialogNode,
    DialogNodeOverride,
    DialogOption,
    FormulaGlobal,
    GlobalTrigger,
    GlobalTriggerEffect,
    ItemReaction,
    ItemType,
    collect_records,
    generate_id
)

def define_hints():
    crops = [('turnip_mature', 'turnip'),
             ('corn_ripe', 'corn')]

    for crop_mature, crop_result in crops:
        DialogNodeOverride('enterOverworld',
                           dialog_id=f'reeve_enterOverworld_{crop_result}',
                           fReq=' * '.join([
                               'partyOrCrew:reeve',
                               'g1:D_class_balancer2',
                               f'g1:num_{crop_mature}_harvested',
                               DialogNodeOverride.NOT_SEEN_THIS,
                           ]),
                           speakerOverride='reeve',
                           statements=[
                               ('happy', f'''Commodore, we've harvested a <itemName={crop_result}>!'''),
                               'We should show it to Roland in Fantlin.'
                           ])

    DialogNodeOverride('enterOverworld',
                       dialog_id='reeve_enterOverworld_ambushes',
                       fReq=' * '.join([
                           'partyOrCrew:reeve',
                           'g1:D_class_balancer2',
                           'gIsMoreThan:num_crop_harvest_ambushes:4',
                           DialogNodeOverride.NOT_SEEN_THIS,
                       ]),
                       speakerOverride='reeve',
                       statements=[
                           ('angry', 'Commodore, these pests attacking our crops are getting out of hand!'),
                           ('sly', 'Perhaps Roland in Fantlin knows a way to help protect them.')
                       ])


def define_buy_seeds(crop_seeds):
    buy_seeds = DialogNode('crops_buy_seeds',
                           statements=[
                               f'I can give you 10 seeds for $100.',
                               ('sly', '''Of course, there's probably some way you could get more yourself...''')
                           ])
    for seeds in crop_seeds:
        buy_seeds.add_option(f'Buy 10 <itemName={seeds}> ($100)', '',
                             specialEffect=[
                                 'subtract100gp',
                                 f'giveItem,{seeds},10',
                             ],
                             formulaReq='m:money - 99')
    buy_seeds.add_option('<color=SlateGray>Can\'t afford it...',
                         'previous',
                         formulaReq='100 - m:money')
    buy_seeds.add_option('No', 'previous', bottomOption=True)
    return buy_seeds

def define_report_crops():
    report = (
        DialogNode('crops_report',
                   statements=[
                       'What do you have for me?'
                   ])
        .add_option('Give<itemBig=turnip> <itemName=turnip>', DialogNode('crops_report_gave_turnip',
                                                                         statements=[
                                                                             ('happy', 'Hey, a turnip!'),
                                                                             ('sly', 'I knew one of these would eventually turn up.'),
                                                                             '''Watering is kind of a hassle, isn't it?''',
                                                                             '''Well, I've got an improved watering can for you!''',
                                                                             '''Keep up the good work. I'm rooting for you.'''
                                                                         ],
                                                                         specialEffect=[
                                                                             'removeItemFromParty,turnip,1',
                                                                             'giveItem,watering_can_iron,1'
                                                                         ]),
                    formulaReq='gIs0:D_crops_report_gave_turnip * partyItem:turnip')
        .add_option('Give 10<itemBig=turnip> <itemName=turnip>', DialogNode('crops_report_gave_10_turnip',
                                                                            statements=[
                                                                                ('sigh', '''More turnips... hurray...'''),
                                                                                ('concern', 'Look, if I give you this watering can schematic, will you stop unloading turnips on me?'),
                                                                                '''I'm rutabegging you!'''
                                                                            ],
                                                                            specialEffect=[
                                                                                'removeItemFromParty,turnip,10',
                                                                                'giveItem,craft_watering_can,1'
                                                                            ]),
                    formulaReq='gIs1:D_crops_report_gave_turnip * gIs0:D_crops_report_gave_10_turnip * partyItem:turnip - 9')
        .add_option('Give<itemBig=corn> <itemName=corn>', DialogNode('crops_report_gave_corn',
                                                                     statements=[
                                                                         ('happy', 'Wow, corn! Good job.'),
                                                                         '''Here's a tool that should help you harvest corn faster.''',
                                                                         'With more samples, I should be able to make the design available for publication.'
                                                                     ],
                                                                     specialEffect=[
                                                                         'removeItemFromParty,corn,1',
                                                                         'giveItem,scythe_wood,1'
                                                                     ]),
                    formulaReq='gIs0:D_crops_report_gave_corn * partyItem:corn')
        .add_option('Give 10<itemBig=corn> <itemName=corn>', DialogNode('crops_report_gave_10_corn',
                                                                        statements=[
                                                                            ('happy', '''You sure do like growing corn, don't you?'''),
                                                                            '''I've just put the finishing touches on the scythe schematics.''',
                                                                            'I want you to have the first copy.'
                                                                        ],
                                                                        specialEffect=[
                                                                            'removeItemFromParty,corn,10',
                                                                            'giveItem,craft_scythe,1'
                                                                        ]),
                    formulaReq='gIs1:D_crops_report_gave_corn * gIs0:D_crops_report_gave_10_corn * partyItem:corn - 9')
        .add_option('Pests keep attacking my crops!', DialogNode('crops_report_pests',
                                                                 statements=[
                                                                     ('concern', 'Yes, many creatures do enjoy the taste of fresh vegetables, and not just humanoids.'),
                                                                     'Perhaps what your garden needs is a fence to keep the pests at bay.',
                                                                     '''Here are instructions for building a fence. You'll need a lot of wood, depending on the size of your garden.''',
                                                                     '''There are also steps for making the fence posts connect to each other nicely, if you care about that kind of thing.''',
                                                                     '''Just keep applying the instructions until you like the resulting shape.'''
                                                                 ],
                                                                 specialEffect=[
                                                                     'giveItem,craft_fence,1'
                                                                 ]),
                    formulaReq='gIs0:D_crops_report_pests * gIsMoreThan:num_crop_harvest_ambushes:4')
        .add_option('Nevermind', 'previous', bottomOption=True)
    )
    return report


def define_roland_extra_dialog():
    crop_seeds = ['turnip_seeds', 'corn_seeds', 'wheat_seeds']

    DialogOption('How can I help?', DialogNode('crops_offer_help',
                                               statements=[
                                                   ('happy', '''You want to help in my research? That's fantastic to hear!'''),
                                                   'Take these seeds and plant them around the world.',
                                                   'If you manage to grow them, please report your findings back to me.',
                                                   ('sigh', 'Unfortunately, those are all I can afford to give away. I can offer more for sale though.'),
                                                   '''Oh, and don't forget to water your seeds. Here's a watering can.'''
                                               ],
                                               specialEffect=[
                                                   'giveItem,watering_can_wood,1'
                                               ] + [
                                                   f'giveItem,{seeds},2' for seeds in crop_seeds
                                               ]),
                 formulaReq='gIs0:D_crops_offer_help',
                 ID='class_balancer2')

    DialogOption('Goodbye', '',
                 ID='class_balancer2',
                 bottomOption=True)

    DialogOption(f'Buy seeds', define_buy_seeds(crop_seeds),
                 formulaReq='gIs1:D_crops_offer_help',
                 newLineOfOptions=True,
                 ID='class_balancer2')

    DialogOption(f'Report', define_report_crops(),
                 formulaReq='gIs1:D_crops_offer_help',
                 newLineOfOptions=True,
                 ID='class_balancer2')

def define_dialogs():
    with collect_records() as c:
        define_hints()
        define_roland_extra_dialog()
        return c
