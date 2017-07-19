-------------------------------------------------------------------------------------------------------
@Code folder
-------------------------------------------------------------------------------------------------------
Pig
-------------------------------------------------------------------------------------------------------
DeleteDuplicateHeading.pig:
Delete duplicate heading in game data.

ReplacingWithAvg.pig:
Replace missing values with average value.

ReplacingWithZero.pig:
Replace missing values with zero value.

* All the data the codes need is in the same folder
-------------------------------------------------------------------------------------------------------
Hive
-------------------------------------------------------------------------------------------------------
I. Following four txt files are the major coding parts.
1. ballgamestep.txt includes the hive code to generate a 5-year baseball game record table for a certain baseball team.
2. bosweatherstep.txt includes the code to generate a 5 years’ weather record.
3. joinstep.txt includes the code to output right outer join query to local. The output file is data.cv.
4. dataParser.py will transfer the output at step 3 to a standard cvs file, dataProcessed.csv.
II.Other txt files are the scripts when running on hdfs.
-------------------------------------------------------------------------------------------------------
MapReduce
-------------------------------------------------------------------------------------------------------
GameWeatherJoin.java: 
Using MapReduce Join to combine weather and game data

* All the data the codes need is in the same folder
-------------------------------------------------------------------------------------------------------
Spark
-------------------------------------------------------------------------------------------------------
StringIndexerOneHotEncoder.py: 
Transform column type string into type nominal 

ChiSqSelector.py: 
Select top 10 features in our data

LinearRegression.py: 
Select the features from ChiSqSelector and run Linear Regression model

DecisionTreeRegressor.py: 
Select the features from ChiSqSelector and run Decision Tree Regression model

RandomForestRegressor.py: 
Select the features from ChiSqSelector and run Random Forest Regression model

* All the data the codes need is in the same folder



-------------------------------------------------------------------------------------------------------
@Screenshot folder
-------------------------------------------------------------------------------------------------------
All the codes have executed screenshots except Hive since we executed Hive in shell mode.
The progresses of Hive are under the folder Code/Hive.
