# D&D Character Generator

import random
import json




class Character():

    def __init__(self):
        # Roll initial abilities
        self.abilities = {
            "str": rollStat(),
            "dex": rollStat(),
            "con": rollStat(),
            "int": rollStat(),
            "wis": rollStat(),
            "cha": rollStat()
                          }

        self.race = selectRace()

        race_data = getRaceData(self.race)

        self.abilityModifier(race_data)

        self.age, self.age_group = self.getAge(race_data)
        self.height, self.weight = self.getSize(race_data)

        self.speed = race_data['speed']
        self.weapon_proficiency = race_data['weapon_proficiency']
        self.tool_proficiency = race_data['tool_proficiency']
        self.armor_proficiency = race_data['armor_proficiency']
        self.languages = race_data['languages']
        self.traits = race_data['traits']
        self.alignment = self.getAlignment(race_data['alignment_affinity'])

        if race_data['subrace']: 
            self.subrace = random.choice(list(race_data['subrace'].keys()))
            try:
                self.abilityModifier(race_data['subrace'][self.subrace])
            except: 
                pass

            try:
                for trait in race_data['subrace'][self.subrace]['traits']:
                    self.traits.append(trait)
            except:
                pass


        
        print(self.race)
        try: 
            print(self.subrace)
        except:
            pass
        print(self.abilities)
        print(f"Age: {self.age}. This is an {self.age_group} {self.race}. They normally reach adulthood at {race_data['age']['adult']} and live to be about {race_data['age']['max']}")
        print(f"Height: {self.height} inches. Weight: {self.weight} lbs.")
        print(f"Alignment: {self.alignment}")
        print(f"Speed: {self.speed}")
        print(f"Languages: {self.languages}")
        print(f"Weapon Proficiency: {self.weapon_proficiency}")
        print(f"Armor Proficiency: {self.armor_proficiency}")
        print(f"Tool Proficiency: {self.tool_proficiency}")
        print(self.traits)


    def abilityModifier(self, data_dict:dict):
        for mod,val in data_dict['score_mod'].items():
            self.abilities[mod] += val
        return

    def getAge(self, data):
        age_group = random.choice(["adult", "adult", "adult", "adult","adult","middle aged", "middle aged", "middle aged", "elder", "venerable", "young"])

        age_min = data['age']['adult']
        age_max = data['age']['max']

        phase_middle = data['age']['phases']['middle']
        phase_old = data['age']['phases']['old']
        phase_venerable = data['age']['phases']['venerable']

        if age_group == "adult":
            age = random.randint(age_min,phase_middle)
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
            age = random.randint(round(age_min/2),age_min)
            return age, age_group

    def getSize(self, data):
        size_stats = data['size']
        h_mod = sum(rollDice(size_stats['height_mod'][0], size_stats['height_mod'][1]))
        height = size_stats['height_base'] + h_mod
        w_mod = sum(rollDice(size_stats['weight_mod'][0], size_stats['weight_mod'][1]))
        weight = size_stats['weight_base'] + (w_mod * h_mod)
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
            "chaotic evil"
        ]

        try:
            for affinity in affinities:
                alignments.append(affinity)
                alignments.append(affinity)
                alignments.append(affinity)
        except: 
            pass

        return random.choice(alignments)



def rollDice(numDice: int, sides:int):
    """
    Roll a several mult-sided dice of choice. 
    """
    return random.sample(range(1,sides+1),numDice)

def rollStat():
    """
    Generates an ability score by rolling 4 d6 dice and returning the sum of the 3 highest rolls. 
    """
    stat = rollDice(4,6)
    stat.sort(reverse=True)
    value = sum(stat[:-1])
    return value


def selectRace():
    f = open('dnd_races.json')
    data = json.load(f)
    return random.choice(list(data['dnd_races'].keys()))
    f.close()

def getRaceData(race):
    """
    Return dict of race data from dnd_races.json
    """
    f = open('dnd_races.json')
    data = json.load(f)
    return data['dnd_races'][race]
    f.close()



char = Character()