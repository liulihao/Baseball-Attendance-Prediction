import pandas as pd
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.ml import Pipeline
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorIndexer, VectorAssembler
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.evaluation import RegressionEvaluator
 
sc = SparkContext()
sql_sc = SQLContext(sc)
pandas_df = pd.read_csv('data.csv')
spark_df = sql_sc.createDataFrame(pandas_df)

df_columns = ["Gm#","MeanTemperatureF","MeanHumidity","MeanVisibilityMiles","MeanWindSpeedMPH","Weekend","D/N","Promotion","W","L","Rank","GB"]
#df_columns = spark_df[:-1]

assembler = VectorAssembler(inputCols = df_columns, outputCol = "features")
vector_df = assembler.transform(spark_df)
data = vector_df.select("features", "Attendance")
featureIndexer = VectorIndexer(inputCol="features", outputCol="indexedFeatures", maxCategories=4).fit(data)

(trainingData, testData) = data.randomSplit([0.7, 0.3])

rf = RandomForestRegressor(featuresCol="indexedFeatures", labelCol="Attendance")
pipeline = Pipeline(stages=[featureIndexer, rf])
model = pipeline.fit(trainingData)

# Make predictions.
predictions = model.transform(testData)
predictions.select("features", "Attendance", "prediction").show(5)

# Select example rows to display.
evaluator_rmse = RegressionEvaluator(labelCol="Attendance", predictionCol="prediction", metricName="rmse")
evaluator_mse = RegressionEvaluator(labelCol="Attendance", predictionCol="prediction", metricName="mse")
evaluator_r2 = RegressionEvaluator(labelCol="Attendance", predictionCol="prediction", metricName="r2")
evaluator_mae = RegressionEvaluator(labelCol="Attendance", predictionCol="prediction", metricName="mae")

rmse = evaluator_rmse.evaluate(predictions)
mse = evaluator_mse.evaluate(predictions)
r2 = evaluator_r2.evaluate(predictions)
mae = evaluator_mae.evaluate(predictions)

print("Random Forest Regression result:")
print("Root Mean Squared Error (RMSE): %g" % rmse)
print("Mean Squared Error (MSE): %g" % mse)
print("Mean Absolute Error (MAE): %g" % mae)
print("R-squared: %g" % r2)

# summary only
treeModel = model.stages[1]
print(treeModel)