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
        kit.recipe('iron_chunk', 'watering_can_iron')
        kit.recipe('steel_bar', 'watering_can_steel')
        kit.recipe('mythril_chunk', 'watering_can_mythril')

        return c

if __name__ == '__main__':
    with collect_records() as c:
        define_watering_can()
        print(c.serialize())
