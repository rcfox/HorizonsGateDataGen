from boatlib.data import (
    Action,
    ActionAOE,
    AvAffecter,
    AvAffecterAOE,
    FURNACE_IDS,
    ItemReaction,
    ItemType,
    collect_records,
)

def define_watering_can():
    affecter_aoe = AvAffecterAOE(shape=3,
                                 aoeCasterAsOrigin=True,
                                 coneAngle=92,
                                 minRange=1,
                                 maxRange=0,
                                 maxRangeBonus=0,
                                 maxRangeAddDistanceFromCaster=True)
    with collect_records() as c:
        iron = ItemType('watering_can_iron',
                        name='Iron Watering Can',
                        texture='rcfox_farming_tools',
                        sprite=0,
                        spriteWhenHeld=1,
                        pR='pIron', pB='pIronHilt',
                        itemCategory='weapon',
                        element='water',
                        harmful=False,
                        special='cannotBeSheathed',
                        weight=2,
                        volume=5,
                        value=25,
                        power=2,
                        action=Action('watering_can_use',
                                      name='Watering Can',
                                      casterAnimation='use',
                                      casterAnimationDependsOnWeaponHand=True,
                                      special='cantUseInCombat',
                                      aoe=ActionAOE(
                                          shape=2,
                                          needsLoS=False,
                                          needsLoE=True,
                                          airborne=True,
                                          arc=True,
                                          minRange=0,
                                          maxRange=0,
                                          maxRangeBonus='w:power + cIsGreaterThan:skill_Ice:6'
                                      ),
                                      av_affecters=[
                                          AvAffecter(aoe=affecter_aoe,
                                                     harmful=False,
                                                     actorValue='wet',
                                                     magnitude=1,
                                                     duration=150,
                                                     chance='d:iceAcc',
                                                     element='water'),
                                          AvAffecter(aoe=affecter_aoe,
                                                     harmful=False,
                                                     actorValue='summonItem',
                                                     magnitude='puddle',
                                                     duration=1,
                                                     chance=100),

                               ])
        )
        wood = ItemType('watering_can_wood',
                        cloneFrom='watering_can_iron',
                        name='Wooden Watering Can',
                        pR='pWood', pB='pWoodDark',
                        power=1)
        steel = ItemType('watering_can_steel',
                         cloneFrom='watering_can_iron',
                         name='Steel Watering Can',
                         pR='pSteel', pB='pSteelHilt',
                         power=3)
        mythril = ItemType('watering_can_mythril',
                           cloneFrom='watering_can_iron',
                           name='Mythril Watering Can',
                           pR='pMythril', pB='pMythrilHilt',
                           power=4)

        kit = ItemType('craft_watering_can',
                       cloneFrom='craft_sword',
                       name='Watering Can Crafting Kit',
                       texture='rcfox_farming_tools',
                       sprite=6,
                       description='Combine this with raw material to create a watering can.')
        kit.recipe('woodPlank', wood, reverse_with=FURNACE_IDS)
        kit.recipe('iron_chunk', iron, reverse_with=FURNACE_IDS)
        kit.recipe('steel_bar', steel, reverse_with=FURNACE_IDS)
        kit.recipe('mythril_chunk', mythril, reverse_with=FURNACE_IDS)

        return c

def define_scythe():
    with collect_records() as c:
        iron = ItemType('scythe_iron',
                        name='Iron Scythe',
                        texture='rcfox_farming_tools',
                        sprite=3,
                        pR='pIron', pB='pIronHilt',
                        itemCategory='weapon',
                        element='spear',
                        special=['cannotBeSheathed', 'sprite2xHeight'],
                        weight=2,
                        volume=5,
                        value=25,
                        power=2,
                        action=Action('scythe_attack',
                                      name='Scythe',
                                      casterAnimation='broadswing',
                                      casterAnimationDependsOnWeaponHand=True,
                                      FXChangesWithWeaponHand=True,
                                      FXOnTarget='swipe',
                                      aoe=ActionAOE(cloneFrom='adjacent'),
                                      av_affecters=[
                                          AvAffecter(aoe=AvAffecterAOE(aoeCasterAsOrigin=True,
                                                                       maxRange=1.5,
                                                                       coneAngle=90),
                                                     actorValue='HP',
                                                     magnitude='d:spearDmg',
                                                     chance='d:spearAcc',
                                                     element=['melee', 'physical', 'slash']),
                                      ])
        )
        wood = ItemType('scythe_wood',
                        cloneFrom='scythe_iron',
                        name='Wooden Scythe',
                        pR='pWood', pB='pWoodDark',
                        power=1)
        steel = ItemType('scythe_steel',
                         cloneFrom='scythe_iron',
                         name='Steel Scythe',
                         pR='pSteel', pB='pSteelHilt',
                         power=3)
        mythril = ItemType('scythe_mythril',
                           cloneFrom='scythe_iron',
                           name='Mythril Scythe',
                           pR='pMythril', pB='pMythrilHilt',
                           power=4)

        kit = ItemType('craft_scythe',
                       cloneFrom='craft_sword',
                       name='Scythe Crafting Kit',
                       texture='rcfox_farming_tools',
                       sprite=6,
                       description='Combine this with raw material to create a scythe.')
        kit.recipe('woodPlank', wood, reverse_with=FURNACE_IDS)
        kit.recipe('iron_chunk', iron, reverse_with=FURNACE_IDS)
        kit.recipe('steel_bar', steel, reverse_with=FURNACE_IDS)
        kit.recipe('mythril_chunk', mythril, reverse_with=FURNACE_IDS)

        return c

if __name__ == '__main__':
    with collect_records() as c:
        define_watering_can()
        define_scythe()
        print(c.serialize())
