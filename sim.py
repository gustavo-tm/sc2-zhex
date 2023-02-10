import json

class Game:
    def __init__(self, show = True, history = [], auto_skip = True):

        self.time = 0
        self.minerals = 0
        self.nsupply = 0
        self.show = False

        self.building_configs = json.loads(open("buildings.json").read())
        self.start_config = json.loads(open("start_config.json").read())

        self.supply = self.start_config["supply"]
        self.supply_cost = self.start_config["supply_cost"]
        self.buildings = (
            [Building(self.building_configs["extractor"], "extractor", insta_build = True) for _ in range(self.start_config["extractors"])] +
            [Building(self.building_configs["slow"], "slow", insta_build = True) for _ in range(self.start_config["spawners"])]
        )

        self.income_m = 0
        self.calc_income()

        self.save = False
        self.history = history
        self.run_history()
        
        self.auto_skip = auto_skip
        self.show = show
        self.auto_building = False


    def run_history(self):

        for command in self.history:
            eval(command[0])(command[1])
        self.save = True
        if self.show: print(f"""
            Current status
            Time (s): {round(self.time, 2)}, Time (m): {round(self.time / 60, 2)}
            Mineral balance: {round(self.minerals, 2)}
            Supply balance: {round(self.supply, 2)}
            Income: {round(self.income_m, 2)}
            """)


    def undo(self, changes = 1):
        for _ in range(changes):
            self.history.pop()
        self.__init__(history = self.history)
        if self.show: print(f"{changes} change(s) undone.")

    def save_history(self, name = "build_order"):
        with open(f'{name}.txt', 'w') as history:
            history.write(str(self.history))
        if self.show: print(f"Saved build order to {name}.txt")

    def load_history(self, name = "build_order"):
        history = eval(open(f'{name}.txt','r').read())
        self.__init__(history = history)
        if self.show: print(f"Loaded build order from {name}.txt")

    def auto_build(self, condition):
        self.auto_building = True
        self.calc_ratio()
        while condition:
            self.build(self.suggestion)
        self.auto_building = False

    def calc_income(self):

        previous_income = self.income_m
        self.income_m = (
            self.start_config["income_flat"] + (
                sum([built_spawner.built for built_spawner in self.buildings if built_spawner.type == 1]) + self.start_config["spawner_buff"]
            ) * sum([built_extractor.built for built_extractor in self.buildings if built_extractor.type == 0])
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
        if self.minerals >= self.supply_cost:
            self.minerals -= self.supply_cost
            self.supply += 45
            self.supply_cost += 125 * (self.nsupply % 2)
            self.nsupply += 1
            self.history.append(("self.buy_supply()", None))
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
            print(f"""
                Not enough resources.
                Available minerals: {self.minerals}
                Required minerals: {self.supply_cost}
            """)
            if self.auto_skip:
                self.skipm(self.supply_cost - self.minerals)
        
    def build(self, building):
        cost_min = self.building_configs[building]["cost_min"]
        cost_sup = self.building_configs[building]["cost_sup"]
        if self.minerals >= cost_min and self.supply >= cost_sup:
            self.buildings.append(Building(self.building_configs[building], building))
            self.minerals -= cost_min
            self.supply -= cost_sup
            if self.save: self.history.append(("self.build", building))
            if self.show: print(f"""
                Built new structure: {building}
                Updated mineral balance: {self.minerals}
                Updated supply balance: {self.supply}
                """)
        else: 
            print(f"""
                Not enough resources.
                Available minerals: {self.minerals}
                Required minerals: {cost_min}
                Available supply: {self.supply}
                Required supply: {cost_sup}
            """)
            if self.auto_skip:
                if self.supply <= cost_sup:
                    self.buy_supply()
                if self.minerals <= cost_min:
                    self.skipm(cost_min - self.minerals)
                self.build(building)

        if self.show or self.auto_building: self.calc_ratio()

    def skipm(self, minerals):

        if self.save: self.history.append(("self.skipm", minerals))
        while minerals > 0:
            time = minerals / self.income_s
            minerals -= self.skip(time)[1]

        
        if self.show: print(f"""
            Finished skipping.
            Current time: {round(self.time, 2)}
            Mineral balance: {round(self.minerals, 2)}
            """) 

    def skipt(self, time):

        if self.save: self.history.append(("self.skipt", time))
        while time > 0:
            time -= self.skip(time)[0]

        if self.show: print(f"""
            Finished skipping.
            Current time: {round(self.time, 2)}
            Mineral balance: {round(self.minerals, 2)}
            """)

    def skip(self, time):
        time_skip = (
                min([abs(building.time) for building in self.buildings 
                if building.built == False] + [time])) 
        mineral_skip = self.income_s * time_skip

        change = False
        for building in self.buildings:
            building.time += time_skip
            if building.time == 0:
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

game = Game()
