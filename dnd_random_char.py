# D&D Character Generator

import random
import json
from collections import Counter

class Character:
    def __init__(self):
        self.level = 1
        # Roll initial abilities
        self.abilities = {
            "str": rollStat(),
            "dex": rollStat(),
            "con": rollStat(),
            "int": rollStat(),
            "wis": rollStat(),
            "cha": rollStat(),
        }

        #Get Modifiers from Abilities
        self.abilityModifiers = getAbilityModifiers(self.abilities)

        #select character race
        self.race = selectRace()
        self.raceData = getRaceData(self.race)
        self.adjustAbility(self.raceData["score_mod"])
       
        #set race based stats
        self.age, self.age_group = self.getAge(self.raceData)
        self.height, self.weight = self.getSize(self.raceData)

        self.speed = self.raceData["speed"]
        self.weapon_proficiency = self.raceData["weapon_proficiency"]
        self.tool_proficiency = self.raceData["tool_proficiency"]
        self.armor_proficiency = self.raceData["armor_proficiency"]
        self.languages = self.raceData["languages"]
        self.traits = self.raceData["traits"]
        self.alignment = self.getAlignment(self.raceData["alignment_affinity"])

        #check for and initiate potential subraces
        if self.raceData["subrace"]:
            self.subrace = random.choice(list(self.raceData["subrace"].keys()))
            try:
                self.adjustAbility(self.raceData["subrace"][self.subrace])
            except:
                pass

            try:
                for trait in self.raceData["subrace"][self.subrace]["traits"]:
                    self.traits.append(trait)
            except:
                pass
        #initiate class based data
        highestStat = max(self.abilities, key = self.abilities.get)
        self.className, self.classData = selectClass(highestStat)
        self.inventory = []
        self.spells = {}

        self.parseClassData()

    def abilityModifier(self, data_dict: dict):
        for mod, val in data_dict["score_mod"].items():
            self.abilities[mod] += val
        return

    def getAge(self, data):
        age_group = random.choice(
            [
                "adult",
                "adult",
                "adult",
                "adult",
                "adult",
                "middle aged",
                "middle aged",
                "middle aged",
                "elder",
                "venerable",
                "young",
            ]
        )

        age_min = data["age"]["adult"]
        age_max = data["age"]["max"]

        phase_middle = data["age"]["phases"]["middle"]
        phase_old = data["age"]["phases"]["old"]
        phase_venerable = data["age"]["phases"]["venerable"]

        if age_group == "adult":
            age = random.randint(age_min, phase_middle)
            return age, age_group
        elif age_group == "middle aged":
            age = random.randint(phase_middle, phase_old)
            return age, age_group
        elif age_group == "elder":
            age = random.randint(phase_old, phase_venerable)
            return age, age_group
        elif age_group == "venerable":
            age = random.randint(phase_venerable, age_max)
            return age, age_group
        elif age_group == "young":
            age = random.randint(round(age_min / 2), age_min)
            return age, age_group

    def getSize(self, data):
        size_stats = data["size"]
        h_mod = sum(rollDice(size_stats["height_mod"][0], size_stats["height_mod"][1]))
        height = size_stats["height_base"] + h_mod
        w_mod = sum(rollDice(size_stats["weight_mod"][0], size_stats["weight_mod"][1]))
        weight = size_stats["weight_base"] + (w_mod * h_mod)
        if self.age_group == "young":
            height *= 0.75
            weight *= 0.75
        return round(height), round(weight)

    def getAlignment(self, affinities):
        alignments = [
            "lawful good",
            "lawful neutral",
            "lawful evil",
            "neutral good",
            "true neutral",
            "neutral evil",
            "chaotic good",
            "chaotic neutral",
            "chaotic evil",
        ]

        try:
            for affinity in affinities:
                alignments.append(affinity)
                alignments.append(affinity)
                alignments.append(affinity)
        except:
            pass

        return random.choice(alignments)

    def parseClassData(self):
        """
        Transforms json data from classes and turns them into properties for 
        """
        self.hitDie = self.classData['hit_die']
        self.hitPoints = self.classData["hp_base_lv_1"]["init"] + self.abilities[self.classData["hp_base_lv_1"]["modifier"]]
        self.proficiencyBonus = self.classData['proficiency_bonus']

        try:
            for x in self.classData['armor_proficiency']:
                self.armor_proficiency.append(x)
        except:
            pass

        try:
            for x in self.classData['weapon_proficiency']:
                self.weapon_proficiency.append(x)
        except:
            pass

        try:
            for x in self.classData['tool_proficiency']:
                self.tool_proficiency.append(x)
        except:
            pass

        self.savingThrows = self.classData['saving_throw']
        
        self.skillProficiencies = selectSkillProficiency(self.classData['skills']['num'],self.classData['skills']['selection'])
        self.startingInventory()

        try:
            self.spells = self.classData["spells"]
        except:
            pass

        self.features = self.classData['features']
    
    def startingInventory(self):
        itemSelections = self.classData["equipment"]["choices"]

        for selection in itemSelections:
            self.inventory.append(random.choice(selection))

        for item in self.classData["equipment"]["standard"]:
            self.inventory.append(item)
        return

    def selectAndParseSubclass(self):
        subclasses = self.classData["subclass"]
        self.subclassName = random.choice(subclasses.keys())

        if (self.race == "dragonborn") & (self.subclassName == "draconic bloodline"):
            self.subclassName = random.choice(subclasses.keys())

        self.subclassData = self.classData["subclass"][self.subclassName]
        try:
            self.spells.update({"available_spells":{"level 1": self.subclassData["spells"]}})
        except:
            pass

        try:
            for x in self.subclassData['weapon_proficiency']:
                self.weapon_proficiency.append(x)
        except:
            pass

        try:
            for x in self.subclassData['armor_proficiency']:
                self.armor_proficiency.append(x)
        except:
            pass

        try:
            for x in self.subclassData['features']:
                self.features.append(x)
        except:
            pass

    def adjustAbility(self, dictionary):
        for abl, mod in dictionary.items():
            self.abilityModifiers[abl] += mod

    def printCharacterSheet(self):
        try:
            print(f"Level {self.level} {self.race} ({self.subrace}) {self.className} ({self.subclassName})")
        except:
            try: 
                print(f"Level {self.level} {self.race} ({self.subrace}) {self.className}")
            except:
                try:
                    print(f"Level {self.level} {self.race} {self.className} ({self.subclassName})")
                except:
                    print(f"Level {self.level} {self.race} {self.className}")
        print(self.abilities)
        print(self.abilityModifiers)
        print(self.skillProficiencies)
        print(f"Hit Die: {self.hitDie}")
        print(f"Hit Points: {self.hitPoints}")
        print(
            f"Age: {self.age}. This is an {self.age_group} {self.race}. They normally reach adulthood at {self.raceData['age']['adult']} and live to be about {self.raceData['age']['max']}"
        )
        print(f"Height: {self.height} inches. Weight: {self.weight} lbs.")
        print(f"Alignment: {self.alignment}")
        print(f"Speed: {self.speed}")
        print(f"Languages: {self.languages}")
        print(f"Weapon Proficiency: {self.weapon_proficiency}")
        print(f"Armor Proficiency: {self.armor_proficiency}")
        print(f"Tool Proficiency: {self.tool_proficiency}")
        try:
            print(self.spells)
        except:
            pass
        print(self.traits)
        return


def rollDice(numDice: int, sides: int):
    """
    Roll a several mult-sided dice of choice.
    """
    return random.sample(range(1, sides + 1), numDice)


def rollStat():
    """
    Generates an ability score by rolling 4 d6 dice and returning the sum of the 3 highest rolls.
    """
    stat = rollDice(4, 6)
    stat.sort(reverse=True)
    value = sum(stat[:-1])
    return value


def selectRace():
    f = open("dnd_races.json")
    data = json.load(f)
    race = random.choice(list(data["dnd_races"].keys()))
    f.close()
    return race

def selectClass(stat_weight = False):
    f = open("classes.json")
    data = json.load(f)
    classData = data["first level dnd classes"]
    classChoices = list(classData.keys())
    if stat_weight:
        for cla in classData.keys():
            if stat_weight in classData[cla]['saving_throw']:
                classChoices.append(cla)
                classChoices.append(cla)
                classChoices.append(cla)
    charClass = random.choice(classChoices)
    f.close()
    return charClass, classData[charClass]


def getRaceData(race):
    """
    Return dict of race data from dnd_races.json
    """
    f = open("dnd_races.json")
    data = json.load(f)
    f.close()
    return data["dnd_races"][race]

def fightStyleSelector():
    fightingStyles = [
        "Archery. You gain a +2 bonus to attack rolls you make with ranged weapons.",
        "Blind Fighting. You have blindsight with a range of 10 feet. Within that range, you can effectively see anything that isn't behind total cover, even if you're blinded or in darkness. Moreover, you can see an invisible creature within that range, unless the creature successfully hides from you. Defense. While you are wearing armor, you gain a +1 bonus to AC.",
        "Dueling. When you are wielding a melee weapon in one hand and no other weapons, you gain a +2 bonus to damage rolls with that weapon.",
        "Great Weapon Fighting. When you roll a 1 or 2 on a damage die for an attack you make with a melee weapon that you are wielding with two hands, you can reroll the die and must use the new roll, even if the new roll is a 1 or a 2. The weapon must have the two-handed or versatile property for you to gain this benefit.",
        "Interception. When a creature you can see hits a target, other than you, within 5 feet of you with an attack, you can use your reaction to reduce the damage the target takes by 1d10 + your proficiency bonus (to a minimum of 0 damage). You must be wielding a shield or a simple or martial weapon to use this reaction.",
        "Protection. When a creature you can see attacks a target other than you that is within 5 feet of you, you can use your reaction to impose disadvantage on the attack roll. You must be wielding a shield.",
        "Superior Technique. You learn one maneuver of your choice from among those available to the Battle Master archetype. If a maneuver you use requires your target to make a saving throw to resist the maneuver's effects, the saving throw DC equals 8 + your proficiency bonus + your Strength or Dexterity modifier (your choice.) You gain one superiority die, which is a d6 (this die is added to any superiority dice you have from another source). This die is used to fuel your maneuvers. A superiority die is expended when you use it. You regain your expended superiority dice when you finish a short or long rest.",
        "Thrown Weapon Fighting. You can draw a weapon that has the thrown property as part of the attack you make with the weapon. In addition, when you hit with a ranged attack using a thrown weapon, you gain a +2 bonus to the damage roll.",
        "Two-Weapon Fighting. When you engage in two-weapon fighting, you can add your ability modifier to the damage of the second attack.",
        "Unarmed Fighting. Your unarmed strikes can deal bludgeoning damage equal to 1d6 + your Strength modifier on a hit. If you aren't wielding any weapons or a shield when you make the attack roll, the d6 becomes a d8. At the start of each of your turns, you can deal 1d4 bludgeoning damage to one creature grappled by you."

    ]

    return random.choice(fightingStyles)

def dragonAncestorSelector():
    dragons = ["Black Dragon - Acid Damage", "Blue Dragon - Lightning Damage", "Brass Dragon - Fire Damage", "Bronze Dragon - Lightning Damage", "Copper Dragon - Acid Damage", "Gold Dragon - Fire Damage", "Green Dragon - Poison Damage", "Red Dragon - Fire Damage", "Silver Dragon - Cold Damage", "White Dragon - Cold Damage"]

    return random.choice(dragons)

def selectSkillProficiency(numSkills: int, skillList: list):
    return random.sample(skillList, numSkills)

def getAbilityModifiers(abilityDict):
    modifierDict = {}
    for ability, score in abilityDict.items():
        match score:
            case 1:
                modifierDict[ability] = -5
            case 2 | 3:
                modifierDict[ability] = -4 
            case 4 | 5:
                modifierDict[ability] = -3
            case 6 | 7:
                modifierDict[ability] = -2
            case 8 | 9:
                modifierDict[ability] = -1
            case 10 | 11:
                modifierDict[ability] = 0
            case 12 | 13:
                modifierDict[ability] = 1
            case 14 | 15:
                modifierDict[ability] = 2
            case 16 | 17:
                modifierDict[ability] = 3
            case 18 | 19:
                modifierDict[ability] = 4
            case 20 | 21: 
                modifierDict[ability] = 5
            case 22 | 23:
                modifierDict[ability] = 6
            case 24 | 25: 
                modifierDict[ability] = 7
            case 26 | 27:
                modifierDict[ability] = 8
            case 28 | 29:
                modifierDict[ability] = 9
            case _:
                modifierDict[ability] = 10
    return modifierDict



char = Character()
char.printCharacterSheet()
