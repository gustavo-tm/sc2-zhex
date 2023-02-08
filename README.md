# sc2-zhex
### **For non Zerg Hex players:**
Zerg hex is an Arcade mode game made by the StarCraft II community in which two races fight a Tug of War type RTS game. This script is made with intentions of making it easier for the player to create and optimize their strategies.
### **How the script works:**
The script, unlike its predecessor, does not work with a simulation tickspeed, it can actually tick warp. This enables unique behaviours that would take a lot of computational power for the previous iteration, like buying an upgrade when 10k minerals are available - the old script would have to run hundreds or thousands of ticks that increasingly gain complexity. Now, the script can skip the ticks in which none of the components from the income calculations are changed.
$$ income_\text{minute} = 160+\text{extractors}\cdot(30+\text{spawners}) $$
### **Available features**
- ```Game.build(spawner)```: creates a new structure object, could be a slowling, strikeling or extractor. Structures settings are already built-in. More structures will be added
- ```Game.skipm(minerals)```: skips an amount of time to the future. Structures that are being built will finish building, the income will be updated and the amount of minerals will be adjused accordingly.
- ```Game.skipt(time)```: just like