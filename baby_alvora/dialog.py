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

def define_mouth_guards_defeated():
    node = DialogNode(dialog_id='baby_alvora_mouth_guards_defeated',
                      statements=[
                          '''The enemies guarding the mouth have been defeated.''',
                      ])
    node.add_option('Enter the gaping maw of the beast!',
                    DialogNode(specialEffect=['enterBabyAlvora']))
    node.add_option('Return to the ship.',
                    DialogNode(specialEffect=['endBoarding']))

def define_dialogs():
    with collect_records() as c:
        define_mouth_guards_defeated()
        return c
