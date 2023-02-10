# sc2-zhex
### **For non Zerg Hex players:**
Zerg hex is an Arcade mode game made by the StarCraft II community in which two races fight a Tug of War type RTS game. This script is made with intentions of making it easier for the player to create and optimize their strategies.
### **How the script works:**
The script, unlike its predecessor, does not work with a simulation tickspeed, it can actually tick warp. This enables unique behaviours that would take a lot of computational power for the previous iteration, like buying an upgrade when 10k minerals are available - the old script would have to run hundreds or thousands of ticks that increasingly gain complexity. Now, the script can skip the ticks in which none of the components from the income calculations are changed.

$$ income_\text{minute} = 160+\text{extractors}\cdot(30+\text{spawners}) $$

### **Available commands and attributes**
- ```Game.build(spawner)```: creates a new structure object, could be a slowling, strikeling or extractor. Structures settings are already built-in. More structures will be added;
- ```Game.skipt(time)```: skips an amount of time to the future. Structures that are being built will finish building, the income will be updated and the amount of minerals will be adjused accordingly;
- ```Game.skipm(minerals)```: just like skipping time, it is possible to skip a certain amount of minerals to the future.
- ```Game.undo(changes_undone)```: undos the defined amount of features
- ```Game.save_history(name)```: saves the build order to a .txt file
- ```Game.load_history(name)```: loads the build order from an available .txt file on the computer that meets the structure of the history (for instance a build order saved previously)
- ```Game.show ```: When set to "True" (default value), all commands will output a change log along with more informations that could help making the next decision
- ```Game.auto_skip ```: If set to "True" (default value), when there are not enough resources for a command, the script automatically skips in time and aquire those resources

### *Known issues*
- None

### *Planned Features*
- Clone current state: In order to compare two different choices, it would be good to work on them side by side from a point in time, so cloning a current state would make that easier;
- Make build requests: Instead of skipping time and building, a building request and buffer could make it simpler to create an actual build;
- Add inteligence: Working towards the same direction as the previous iteration of the zerg hex simulator, some kind of intelligence that would tell what choice yieds the most income in the long run would be very nice;
- Add analysis: Would be great to visualize the timeline in some kind of plot and add statistics, for instance how much the user deviates from the optimal eco build and how much aggressive potential that build presents on each stage of the game, etc;
- Move the interface to somewhere more user-friendly
