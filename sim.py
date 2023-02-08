import json

class Game:

    def __init__(self):

        self.building_configs = json.loads(open("buildings.json").read())
        self.start_config = json.loads(open("start_config.json").read())

        self.supply = self.start_config["supply"]
        self.supply_cost = self.start_config["supply_cost"]
        self.buildings = (
            [Building(self.building_configs["extractor"], insta_build = True) for _ in range(self.start_config["extractors"])] +
            [Building(self.building_configs["slow"], insta_build = True) for _ in range(self.start_config["spawners"])]
        )

        self.time = 0
        self.minerals = 0
        self.nsupply = 0
        
        self.calc_income()

    def calc_income(self):

        self.income = (
            self.start_config["income_flat"] + (
                sum([built_spawner.built for built_spawner in self.buildings if built_spawner.type == 1]) + self.start_config["spawner_buff"]
            ) * sum([built_extractor.built for built_extractor in self.buildings if built_extractor.type == 0])
        )

    def build(self, building):
        
        self.buildings.append(Building(self.building_configs[building]))
        self.minerals -= self.building_configs[building]["cost_min"]
        self.supply -= self.building_configs[building]["cost_sup"]

    def skipm(self, minerals):
        pass

    def skipt(self, time, show = False):

        while time != 0:

            sinal = time/abs(time)
            time_skip = (
                min([abs(building.time) for building in self.buildings 
                if building.built != (time > 0)] + [abs(time)]) #if time skip is forward in time, only unbuilt structures will be considered
            ) * sinal
            for building in self.buildings:
                building.time += time_skip
                if building.time == time_skip:
                    building.built = (building.built + 1) % 2 #built structures will get unbuilt and unbuilt structures will be built 
            
            self.time += time_skip
            time -= time_skip
            print(time_skip)
        
            self.calc_income()

class Building:

    def __init__(self, building_configs, insta_build = False):

        self.type = building_configs["eco_type"]
        self.cost_min = building_configs["cost_min"]
        self.cost_sup = building_configs["cost_sup"]

        if insta_build:
            self.time = 0
        else:
            self.time = -building_configs["build_time"]

        self.built = self.time >= 0 

game = Game()