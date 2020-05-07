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
                                      casterAnimation='broadswing',
                                      casterAnimationDependsOnWeaponHand=True,
                                      FXChangesWithWeaponHand=True,
                                      FXOnTarget='swipe',
                                      special='cantUseInCombat',
                                      aoe=ActionAOE(cloneFrom='adjacent'),
                                      av_affecters=[
                                          AvAffecter(aoe=AvAffecterAOE(aoeCasterAsOrigin=True,
                                                                       maxRange=1.5,
                                                                       coneAngle=90,
                                                                       maxRangeBonus='w:power - 1'),
                                                     actorValue='HP',
                                                     magnitude='d:spearDmg',
                                                     chance='d:spearAcc',
                                                     element=['slash']),
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
                       sprite=7,
                       description='Combine this with raw material to create a scythe.')
        kit.recipe('woodPlank', wood, reverse_with=FURNACE_IDS)
        kit.recipe('iron_chunk', iron, reverse_with=FURNACE_IDS)
        kit.recipe('steel_bar', steel, reverse_with=FURNACE_IDS)
        kit.recipe('mythril_chunk', mythril, reverse_with=FURNACE_IDS)

        return c

def define_hoe():
    with collect_records() as c:
        iron = ItemType('hoe_iron',
                        name='Iron Hoe',
                        texture='rcfox_farming_tools',
                        sprite=2,
                        pR='pIron', pB='pIronHilt',
                        itemCategory='weapon',
                        element='spear',
                        special=['cannotBeSheathed', 'sprite2xHeight'],
                        weight=2,
                        volume=5,
                        value=25,
                        power=2,
                        action=Action('hoe_attack',
                                      casterAnimation='spear',
                                      casterAnimationDependsOnWeaponHand=True,
                                      FXChangesWithWeaponHand=True,
                                      FXOnTarget='stab',
                                      special='cantUseInCombat',
                                      aoe=ActionAOE(
                                          shape=2,
	                                  needsLoS=True,
	                                  needsLoE=True,
	                                  airborne=True,
	                                  minRange=1,
	                                  maxRange=2,
                                          maxRangeBonus='w:power - 1',
	                                  bypassAll=False,
	                                  occupyAll=False),
                                      av_affecters=[
                                          AvAffecter(aoe=AvAffecterAOE(aoeCasterAsOrigin=True,
                                                                       shape=2,
                                                                       minRange=1,
                                                                       maxRange=0,
                                                                       maxRangeBonus=0,
                                                                       maxRangeAddDistanceFromCaster=True,
                                                                       coneAngle=1),
                                                     actorValue='HP',
                                                     magnitude='d:spearDmg',
                                                     chance='d:spearAcc',
                                                     element=['dig']),
                                      ])
        )
        wood = ItemType('hoe_wood',
                        cloneFrom='hoe_iron',
                        name='Wooden Hoe',
                        pR='pWood', pB='pWoodDark',
                        power=1)
        steel = ItemType('hoe_steel',
                         cloneFrom='hoe_iron',
                         name='Steel Hoe',
                         pR='pSteel', pB='pSteelHilt',
                         power=3)
        mythril = ItemType('hoe_mythril',
                           cloneFrom='hoe_iron',
                           name='Mythril Hoe',
                           pR='pMythril', pB='pMythrilHilt',
                           power=4)

        kit = ItemType('craft_hoe',
                       cloneFrom='craft_sword',
                       name='Hoe Crafting Kit',
                       texture='rcfox_farming_tools',
                       sprite=12,
                       description='Combine this with raw material to create a hoe.')
        kit.recipe('woodPlank', wood, reverse_with=FURNACE_IDS)
        kit.recipe('iron_chunk', iron, reverse_with=FURNACE_IDS)
        kit.recipe('steel_bar', steel, reverse_with=FURNACE_IDS)
        kit.recipe('mythril_chunk', mythril, reverse_with=FURNACE_IDS)

        return c

def define_craftable_fences():
    with collect_records() as c:
        original_wood_fence_types = ['fence_Mid', 'fence_NW', 'fence_N', 'fence_NE',
                                     'fence_E', 'fence_SE', 'fence_SW', 'fence_W']
        wood_fences = [
            ItemType(f'{fence_type}_crafted',
                     cloneFrom=fence_type,
                     description='Use an axe to chop it down or break it with a physical attack.',
                     reactions=[
                         ItemReaction(element='heavySlash', newID='woodPlank'),
                         ItemReaction(element='physical',
                                      aiRatingMod=100,
                                      aiRatingModForHostilesOnly=True,
                                      newID=ItemType(f'{fence_type}_crafted_weak',
                                                     cloneFrom=fence_type,
                                                     pB='zoneWoodDark',
                                                     description='Looks like it will break with one more hit.',
                                                     reactions=[
                                                         ItemReaction(element='physical',
                                                                      newID='X',
                                                                      aiRatingMod=100,
                                                                      aiRatingModForHostilesOnly=True)
                                                     ]))
                     ])
            for fence_type in original_wood_fence_types
        ]


        kit = ItemType('craft_fence',
                       cloneFrom='craft_sword',
                       name='Fence Crafting Kit',
                       texture='rcfox_farming_tools',
                       sprite=13,
                       description='Combine this with wood planks to create a fence, or with a fence to change the fence direction.')
        kit.recipe('woodPlank', wood_fences[0])
        for fence1, fence2 in zip(wood_fences, wood_fences[1:] + wood_fences[:1]):
            kit.recipe(fence1.id, fence2.id)

def define_tools():
    with collect_records() as c:
        define_watering_can()
        define_scythe()
        define_hoe()
        define_craftable_fences()
        return c

if __name__ == '__main__':
    print(define_tools().serialize())
