# Team_Arjan - RailNL

***Heuristieken spring 2018.***

### The case

The Dutch railway system is really extensive, and a very important part of Dutch culture. The trains stop at almost every (major) city in the Netherlands, and no railway system in the EU is as busy as the one in the Netherlands (source: [NU.nl](https://www.nu.nl/weekend/3894182/125-jaar-amsterdam-centraal-van-300-300000-reizigers.html?redirect=1)). 

The routes that the NS (Dutch Railway Company) travels accross, are in no doubt carefully selected. We were challenged to create a new set of routes for RailNL, the (fictional) rival company of the NS.

RailNL wanted us to tackle this problem in steps: Start small, and go bigger and bigger along the way. We started with the task of creating a set of routes for two of the biggest provinces: Noord-Holland and Zuid-Holland. In this province, RailNL selected the 22 most important stations, and deemed seven of these stations critcal. This means that these stations are a key part of the railway system, meaning that trains have to travel to these stations regularly. We were allowed to use seven trains, and all the routes had to be fall in a time limit of 120 minutes (2 hours). 

The second task meant that suddenly, all stations in Noord-Holland and Zuid-Holland were critical (meaning the 22 selected stations). 

After this, we moved on the the bigger picture: The whole country of the Netherlands. In this scenario, our task was to connect a total of 61 stations, of which 23 were critical. For this task, we had a total of 20 trains at our disposal, and we were to finish all routes within the timeframe of 180 minutes (3 hours). 

Once again, after solving the above task, we made all the stations critical.

#### How good is the set of routes?

To determine how well the routes we created fit the requirements of RailNL, we were given the following score function. 

`S = p*10000 - (t*20 + min/10)`

We tackled the tasks by writing algorithms that would create a set of routes. The algorithms can be found in the `algorithm` folder. 

For more information abot the case, see the [Heuristieken wiki](http://heuristieken.nl/wiki/index.php?title=RailNL). 


### File structure:

The files are structured in folders with names that describe their contents.
For example, the python code is in the folder Code and the input data is in the folder Data etc.

### How to (test):

In order to use the code with standard configuration, use the following code for an instruction guide:

`python main.py`


#### Command-line options:

The following arguments can be given:

| Command-Line Argument | Purpose|
|----------------------|------------------------------|
| `-a` or `--algorythm` |	Specify which algorythm to run|
| `-s` or `--scenario` 	|	Specify which scenario to load|
|`-t` or `--times` 		| Specify how many times the algorithm runs|
|`-v` or `--visual` 		| Create visualization |
|`-s` or `--save` 		| Save the output in an .csv file|
|`-i` or `--ignore` 		| Ignore a station. The solution will not include/travel along this station. Input should be a string between quotation makrs. |


Specifying an algorithm is required, the rest of the command-line arguments are optional. 

To run the visualisation you will need to run the following command first:

`pip install -r requirements.txt`
 
## Authors:
Ivo den Hertog, Emma Hokken, and Barry de Vries.
