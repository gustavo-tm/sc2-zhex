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

            self.time_2change = min([-sinal * building.time for building in self.buildings if -sinal * building.time <= 0])

            if abs(time) < self.time_2change:
                self.time += time
                self.minerals += time * self.income/60
                for building in self.buildings:
                    building.time += time
                    building.built = building.time >= 0
            
                if show:
                    print("skipped ", self.time)

                time = 0

            else:
                self.time += self.time_2change
                time +=  self.time_2change * -sinal
                for building in self.buildings:
                    building.time += self.time_2change
                    if building.time == 0:
                        building.built = (building.built + 1) % 2
               
                if show:
                    print("skipped ", self.time_2change, "\n changed built state of structure")
        print(time)
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