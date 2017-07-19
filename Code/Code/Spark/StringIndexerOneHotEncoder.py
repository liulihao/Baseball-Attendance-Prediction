import pandas as pd
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.ml.feature import OneHotEncoder, StringIndexer

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
eventEncoder = OneHotEncoder(dropLast=False, inputCol="EventsIndex", outputCol="EventVec")
dayEncoder = OneHotEncoder(dropLast=False, inputCol="DayIndex", outputCol="DayVec")
oppEncoder = OneHotEncoder(dropLast=False, inputCol="OppIndex", outputCol="OppVec")
streakEncoder = OneHotEncoder(dropLast=False, inputCol="StreakIndex", outputCol="StreakVec")

eventEncoder = eventEncoder.transform(forthIndexed)
dayEncoder = dayEncoder.transform(eventEncoder)
oppEncoder = oppEncoder.transform(dayEncoder)
streakEncoder = streakEncoder.transform(oppEncoder)

final_df = streakEncoder
final_df.printSchema()
final_df.select("EventVec","DayVec","OppVec","StreakVec").show()
