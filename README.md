# sc2-zhex
### **For non Zerg Hex players:**
Zerg hex is an Arcade mode game made by the StarCraft II community in which two races fight a Tug of War type RTS game. This script is made with intentions of making it easier for the player to create and optimize their strategies.
### **How the script works:**
The script, unlike its predecessor, does not work with a simulation tickspeed, it can actually tick warp. This enables unique behaviours that would take a lot of computational power for the previous iteration, like buying an upgrade when 10k minerals are available - the old script would have to run hundreds or thousands of ticks that increasingly gain complexity. Now, the script can skip the ticks in which none of the components from the income calculations are changed.

$$ income_\text{minute} = 160+\text{extractors}\cdot(30+\text{spawners}) $$

### **Available features**
- ```Game.build(spawner)```: creates a new structure object, could be a slowling, strikeling or extractor. Structures settings are already built-in. More structures will be added;
- ```Game.skipt(time)```: skips an amount of time to the future. Structures that are being built will finish building, the income will be updated and the amount of minerals will be adjused accordingly;
- ```Game.skipm(minerals)```: just like skipping time, it is possible to skip a certain amount of minerals to the future.

### *Known issues*
- Skipping time or minerals to the past is an intended feature, but the choices are not undone yet
- Supply system is not yet implemented
- Nothing stops the users from going achieving negative mineral values

### *Planned Features*
- Undo button: Undo past changes in some way;
- Clone current state: In order to compare two different choices, it would be good to work on them side by side from a point in time, so cloning a current state would make that easier;
- Make build requests: Instead of skipping time and building, a building request and buffer could make it simpler to create an actual build;
- Save build order: Saving the strategy could make it possible to share or to save the progress in order to continue later more easily;
- Add inteligence: Working towards the same direction as the previous iteration of the zerg hex simulator, some kind of intelligence that would tell what choice yieds the most income in the long run would be very nice;
- Add graphs: Would be great to visualize the timeline in some kind of plot;
- Move the interface to somewhere more user-friendly
