from boatlib.data import (collect_records, DialogNode, DialogNodeOverride,
                          GlobalTrigger, GlobalTriggerEffect, DialogOption,
                          Parser)


def main():
    materials = [('iron', 'iron_chunk'), ('wood', 'woodPlank'),
                 ('steel', 'steel_bar'), ('bone', 'bones1'),
                 ('mythril', 'mythril_chunk'), ('coral', 'coral'),
                 ('corpryst', 'corpryst'), ('volskarn', 'volskarn_chunk'),
                 ('leaf', 'aldleaf'), ('silk', 'silk_spide'),
                 ('elec', 'shock_chunk'), ('laser', 'laser_chunk'),
                 ('ironice', 'ironice_chunk'), ('wind', 'whistle_chunk'),
                 ('fang', 'fang_spidest')]
    items = [
        'dagger', 'sword', 'hammer', 'axe', 'shield', 'flail', 'whip', 'bow',
        'xbow', 'spear', 'knuckle', 'rapier', 'greatsword', 'armor'
    ]

    with collect_records() as c:
        recycle_menu = DialogNode(
            'rcfox_smithy_recycle',
            statements=[
                'I can recycle large quantities of equipment into their base components.',
                'All items of a given material that are <color=Blue>held by crew<color=> or <color=Blue>in the stash<color=> will be disassembled.',
                'Beware though: <color=DarkRed>any augments will be lost!<color=><n=>Either drop any items you wish to keep or manually remove the augments at the anvil.'
            ])
        recycle_menu.add_option('Nevermind', '', bottomOption=True)

        DialogOption('Recycle Equipment',
                     recycle_menu,
                     ID='sport_merchant_smithy')

        DialogOption('Goodbye',
                     '',
                     ID='sport_merchant_smithy',
                     bottomOption=True)

        for material, ingredient in materials:
            material_items = [f'{item}_{material}' for item in items]
            material_items.append(f'xbow_{material}_unloaded')

            for item in material_items:
                GlobalTrigger(
                    f'rcfox_recycle_{item}',
                    [
                        GlobalTriggerEffect(
                            'removeItemFromParty', strings=[item], floats=[1]),
                        GlobalTriggerEffect(
                            'giveItem', strings=[ingredient], floats=[1]),
                        GlobalTriggerEffect(
                            'trigger',
                            strings=[f'rcfox_recycle_{item}'],
                            # Adding a tiny delay prevents a stack overflow
                            delay=0.001)
                    ],
                    reqFormula=f'partyItem:{item}')
            material_trigger = GlobalTrigger(f'rcfox_recycle_all_{material}', [
                GlobalTriggerEffect('trigger',
                                    strings=[f'rcfox_recycle_{item}'])
                for item in material_items
            ])

            recycle_menu.add_option(
                material.title(),
                '',
                specialEffect=[f'trigger,{material_trigger.id}'],
                formulaReq=' + '.join(f'partyItem:{item}'
                                      for item in material_items))
        return c.serialize()


if __name__ == '__main__':
    print(main())
