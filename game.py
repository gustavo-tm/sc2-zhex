import json
import numpy as np

class Building:
    def __init__(self, building_configs, name, insta_build = False):

        self.name = name
        self.type = building_configs["eco_type"]
        self.cost_min = building_configs["cost_min"]
        self.cost_sup = building_configs["cost_sup"]

        if insta_build:
            self.time = 0
            self.built = True
        else:
            self.time = -building_configs["build_time"]
            self.built = False

class Game:
    def __init__(self, show = False, auto_skip = True, start_config = json.loads(open("start_config.json").read()), change_stop = False):

        self.time = 0
        self.minerals = 0
        self.nsupply = 0
        self.show = False

        self.building_configs = json.loads(open("buildings.json").read())
        self.start_config = start_config

        self.supply = self.start_config["supply"]
        self.supply_cost = self.start_config["supply_cost"]
        self.buildings = (
            [Building(self.building_configs["extractor"], "extractor", insta_build = True) for _ in range(self.start_config["extractors"])] +
            [Building(self.building_configs["slow"], "slow", insta_build = True) for _ in range(self.start_config["spawners"])]
        )
        self.nstrikes = 0

        self.income_m = 0
        self.calc_income()

        
        self.auto_skip = auto_skip
        self.change_stop = change_stop
        self.show = show

    def calc_income(self):

        previous_income = self.income_m

        structures_type0 = [structure for structure in self.buildings if structure.type == 0]
        structures_type1 = [structure for structure in self.buildings if structure.type == 1]

        self.nstructures_type0 = len(structures_type0)
        self.nstructures_type1 = len(structures_type1)

        self.building_type0 = sum([(structure.built - 1) * structure.time for structure in structures_type0])
        self.building_type1 = sum([(structure.built - 1) * structure.time for structure in structures_type1])

        self.income_m = (
            self.start_config["income_flat"] + (self.nstructures_type1 + self.start_config["spawner_buff"]) * self.nstructures_type0
        )

        self.income_s = self.income_m / 60

        if self.show: print(f"""
            Previous income: {previous_income}
            New income: {self.income_m}
            Income change: {self.income_m - previous_income}
            """)

    def calc_ratio(self):
        marginal_gain_extractor = len([building for building  in self.buildings if building .type == 1]) + self.start_config["spawner_buff"]
        marginal_gain_spawner = len([building for building  in self.buildings if building .type == 0])

        marginal_cost_extractor = (self.building_configs["extractor"]["cost_min"] + 
            (self.building_configs["extractor"]["cost_sup"] / 45) * self.supply_cost)

        min_marginal_cost_spawner, min_marginal_cost = ("", 0) 
        for structure in [building for building in self.building_configs.keys() if building != "extractor"]:
            marginal_cost = (self.building_configs[structure]["cost_min"] + (self.building_configs[structure]["cost_sup"] / 45) * self.supply_cost)
            if min_marginal_cost == 0 or min_marginal_cost > marginal_cost:
                min_marginal_cost = marginal_cost
                min_marginal_cost_spawner = structure

        ROI_extractor = marginal_gain_extractor / marginal_cost_extractor
        ROI_spawner = marginal_gain_spawner / min_marginal_cost
        
        if self.show: print(f"""
            Extractor's ROI: {round(ROI_extractor, 2)}
            Spawner's ROI: {round(ROI_spawner, 2)}
            Cheapest spawner: {min_marginal_cost_spawner}
            """)

        self.suggestion = min_marginal_cost_spawner if ROI_spawner > ROI_extractor else "extractor"

    def buy_supply(self):
        if round(self.minerals, 40) >= self.supply_cost:
            self.minerals -= self.supply_cost
            self.supply += 45
            self.supply_cost += 125 * (self.nsupply % 2)
            self.nsupply += 1
            if self.show: print(f"""
                Bought new supply.
                Time (s): {round(self.time, 2)}, Time (m): {round(self.time / 60, 2)}
                Available supply: {self.supply}
                Supply number: {self.nsupply}
                Supply cost: {self.supply_cost - 125 * ((self.nsupply - 1) % 2)}
                Next supply cost: {self.supply_cost}
                Available minerals: {round(self.minerals, 2)}
                """)
        else: 
            if self.show: print(f"""
                Not enough resources.
                Available minerals: {self.minerals}
                Required minerals: {self.supply_cost}
            """)
            if self.auto_skip:
                self.skipm(self.supply_cost - self.minerals)
                if not self.change_stop: self.buy_supply()
        
    def build(self, building):
        cost_min = self.building_configs[building]["cost_min"]
        cost_sup = self.building_configs[building]["cost_sup"]
        if round(self.minerals, 40) >= cost_min and self.supply >= cost_sup:
            self.buildings.append(Building(self.building_configs[building], building))
            self.nstrikes += 1
            self.minerals -= cost_min
            self.supply -= cost_sup
            if self.show: print(f"""
                Built new structure: {building}
                Updated mineral balance: {self.minerals}
                Updated supply balance: {self.supply}
                """)
        else: 
            if self.show: print(f"""
                Not enough resources.
                Available minerals: {self.minerals}
                Required minerals: {cost_min}
                Available supply: {self.supply}
                Required supply: {cost_sup}
            """)
            if self.auto_skip:
                if self.supply < cost_sup:
                    self.buy_supply()
                if self.minerals < cost_min:
                    self.skipm(cost_min - self.minerals)
                if not self.change_stop: self.build(building)

        if self.show: self.calc_ratio()

    def skipm(self, minerals):

        if self.change_stop:
            time = minerals / self.income_s
            self.skip(time)
        else:
            while round(minerals, 39) > 0:
                time = minerals / self.income_s
                minerals -= self.skip(time)[1]
                if self.show: print(f"""
                    Is skipping minerals.
                    Minerals left: {minerals}
                    Mineral balance: {round(self.minerals, 10)}
                """) 

        if self.show: print(f"""
            Finished skipping.
            Current time: {round(self.time, 2)}
            Mineral balance: {round(self.minerals, 2)}
            """) 

    def skipt(self, time):

        if self.change_stop:
            self.skip(time)
        else:
            while round(time, 39) > 0:
                time -= self.skip(time)[0]

            if self.show: print(f"""
                Finished skipping.
                Current time: {round(self.time, 2)}
                Mineral balance: {round(self.minerals, 2)}
                """)

    def skip(self, time):
        time_skip = (
                min([abs(building.time) for building in self.buildings 
                if building.built == False and building.time != 0] + [time])) 
        mineral_skip = self.income_s * time_skip

        change = False
        for building in self.buildings:
            building.time += time_skip
            if not building.built:
                if building.time >= 0:
                    change = True
                    building.built =True
                    if self.show: print("Structure finished constructing: ", building.name)

        self.time += time_skip
        self.minerals += mineral_skip

        if change: self.calc_income()

        if self.show: print(f"""
            Time skipped: {round(time_skip, 2)}
            Yielded minerals: {round(mineral_skip, 2)}
            Structure state changed: {change}
            """)

        return time_skip, mineral_skip