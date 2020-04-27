
from boatlib.data import (
    Action,
    ActionAOE,
    AvAffecter,
    AvAffecterAOE,
    Collection,
    Duration,
    GlobalTrigger,
    GlobalTriggerEffect,
    ItemReaction,
    ItemType
)

def generate_id(prefix):
    return prefix + str(uuid.uuid4()).replace('-', '')

def callout_action(collection, sayings):
    av_affecters = []
    for say in sayings:
        trigger_id = generate_id('trigger_say_')
        trigger = GlobalTrigger(trigger_id, [
            GlobalTriggerEffect('damageNumber', strings=[say])
        ])
        collection.append(trigger)

        av_affecters.append(AvAffecter(actorValue='trigger',
                                       magnitude=trigger.id,
                                       useSeparateChanceRoll=True,
                                       chance=100 / len(sayings)))

    action_id = generate_id('callout_')
    action = Action(action_id, av_affecters=av_affecters)
    collection.append(action)
    return action

def talking_sword():
    c = Collection()
    sayings = ['Hiya!', 'Take this!', 'Have at you!']
    sword = ItemType('talking_sword',
                     cloneFrom='sword_iron',
                     reactions=[
                         ItemReaction(element='actionTaken', action=callout_action(c, sayings)),
                         ItemReaction(element='itemCombined', action=callout_action(c, ["Aaaaaah! I'm melting!"]))
                     ])
    c.append(sword)
    return c

def lightning_trigger():
    return Action('elecTriggerAttack',
                  name='Lightning Trigger',
                  casterAnimation='spellcast',
                  casterAnimationDependsOnWeaponHand=True,
                  aoe=ActionAOE(cloneFrom='adjacent',
                                arc=True,
                                airborne=True,
                                maxRangeBonus='sa:stoneSavant * 2'),
                  av_affecters=[
                      AvAffecter(actorValue='HP',
                                 magnitude='d:elecDmgWpnPower(0) - sa:stoneSavant * 2',
                                 chance='d:elecAcc',
                                 element=['magic', 'lightning'],
                                 FXOnTile=['lightningStrike_mild', 'shortBolt', 'spark'])
                  ])

def evil_boat():
    action = Action('toyboat_explosion',
                    name='Toy Boat',
                    casterAnimation='use',
                    FXOnTarget=['medShakeHoriz', 'strike'],
                    aoe=ActionAOE(shape=2,
                                  needsLOE=True,
                                  minRange=1,
                                  maxRange=10,
                                  occupyAll=True,
                                  fReq='m:incapped'),
                    av_affecters=[
                        AvAffecter(actorValue='removeActor',
                                   harmful=False,
                                   magnitude=1,
                                   element=['explode', 'smash', 'heavySmash'],
                                   FXOnTile=['sfx_classicExplosion', 'medExplosion', 'ThudShotBigger']),
                        AvAffecter(actorValue='summonItem',
                                   magnitude='loot_bone_junk',
                                   FXOnTile='terrain',
                                   aoe=AvAffecterAOE(cloneFrom='adjacentAndSelf')),
                        AvAffecter(actorValue='push',
                                   useCasterAsOriginForDirectionalEffects=False,
                                   magnitude=3,
                                   chance=100,
                                   FXOnTile='smallShockwave_instant_moving',
                                   aoe=AvAffecterAOE(cloneFrom='adjacent+1',
                                                     arc=True,
                                                     airborne=True,
                                                     coneAngle=360))
                        ])
    boat = ItemType('toyboat', cloneFrom='toyboat', action=action.id)
    return Collection(action, boat)


if __name__ == '__main__':
    print(talking_sword().serialize())
