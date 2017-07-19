import pandas as pd
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler
from pyspark.ml.feature import ChiSqSelector

# Creates Spark Context
sc = SparkContext()
sql_sc = SQLContext(sc)

# Uses panda to read csv file
pandas_df = pd.read_csv('data.csv', na_values=[' '])
spark_df = sql_sc.createDataFrame(pandas_df)

# Step 1 - StringIndexer
firstIndexer = StringIndexer(inputCol="Events", outputCol="EventsIndex")
firstModel = firstIndexer.fit(spark_df)
firstIndexed = firstModel.transform(spark_df)

secondIndexer = StringIndexer(inputCol="D/N", outputCol="DayIndex")
secondModel = secondIndexer.fit(firstIndexed)
secondIndexed = secondModel.transform(firstIndexed)

thirdIndexer = StringIndexer(inputCol="Opp", outputCol="OppIndex")
thirdModel = thirdIndexer.fit(secondIndexed)
thirdIndexed = thirdModel.transform(secondIndexed)

forthIndexer = StringIndexer(inputCol="Streak", outputCol="StreakIndex")
forthModel = forthIndexer.fit(thirdIndexed)
forthIndexed = forthModel.transform(thirdIndexed)

# Step 2 - OneHotEncoder
eventEncoder = OneHotEncoder(dropLast=False, inputCol="EventsIndex", outputCol="EventsVec")
dayEncoder = OneHotEncoder(dropLast=False, inputCol="DayIndex", outputCol="DayVec")
oppEncoder = OneHotEncoder(dropLast=False, inputCol="OppIndex", outputCol="OppVec")
streakEncoder = OneHotEncoder(dropLast=False, inputCol="StreakIndex", outputCol="StreakVec")

eventEncoder = eventEncoder.transform(forthIndexed)
dayEncoder = dayEncoder.transform(eventEncoder)
oppEncoder = oppEncoder.transform(dayEncoder)
streakEncoder = streakEncoder.transform(oppEncoder)

final_df = streakEncoder
df_columns = ["Gm#","MeanTemperatureF","MeanHumidity","MeanVisibilityMiles","MeanWindSpeedMPH","Weekend","Promotion","W","L","Rank","GB","EventsVec","OppVec","DayVec","StreakVec"]

# Step 3 - VectorAssembler
assembler = VectorAssembler(inputCols = df_columns, outputCol = "features")
output = assembler.transform(final_df)
output = output.select("features", "Attendance")

# Step 4 - ChiSqSelector
selector = ChiSqSelector(numTopFeatures = 10, featuresCol = "features", outputCol = "selectedFeatures", labelCol = "Attendance")
result = selector.fit(output).transform(output)
model = selector.fit(output)
result.printSchema()
importantFeatures = model.selectedFeatures

# Shows all important features selected by ChiSqSelector
print("ChiSqSelector with top %d features selected:" % selector.getNumTopFeatures())
for i in range(len(importantFeatures)):
	print importantFeatures[i]

result.show()

sc.stop()
