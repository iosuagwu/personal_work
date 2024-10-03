import findspark
findspark.init()

from pyspark.sql import SparkSession

#import functions/Classes for sparkml

from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.ml.classification import LogisticRegression

# import functions/Classes for metrics
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.clustering import KMeans

#Create SparkSession for Regression Example

spark = SparkSession.builder.appName("Regressing using SparkML").getOrCreate()
# Read in data
mpg_data = spark.read.csv("mpg.csv", header=True, inferSchema=True)
# Prepare feature vector
assembler = VectorAssembler(inputCols=["Cylinders", "Engine Disp", "Horsepower", "Weight", "Accelerate", "Year"], outputCol="features")
mpg_transformed_data = assembler.transform(mpg_data)
# Split data into training and testing sets
(training_data, testing_data) = mpg_transformed_data.randomSplit([0.7, 0.3], seed=42)
# Train linear regression model
lr = LinearRegression(featuresCol="features", labelCol="MPG")
model = lr.fit(training_data)
# Make predictions on testing data
predictions = model.transform(testing_data)
#R-squared (R2): R2 is a statistical measure that represents the proportion of variance
#in the dependent variable (target) that is explained by the independent variables (features).
evaluator = RegressionEvaluator(labelCol="MPG", predictionCol="prediction", metricName="r2")
r2 = evaluator.evaluate(predictions)
print("R Squared =", r2)
#Root Mean Squared Error (RMSE): RMSE is the square root of the average of the squared differences
#between the predicted and actual values. It measures the average distance between the predicted
#and actual values, and lower values indicate better performance.
evaluator = RegressionEvaluator(labelCol="MPG", predictionCol="prediction", metricName="rmse")
rmse = evaluator.evaluate(predictions)
print("RMSE =", rmse)
#Mean Absolute Error (MAE): MAE is the average of the absolute differences between the predicted and
#actual values. It measures the average absolute distance between the predicted and actual values, and
#lower values indicate better performance.
evaluator = RegressionEvaluator(labelCol="MPG", predictionCol="prediction", metricName="mae")
mae = evaluator.evaluate(predictions)
print("MAE =", mae)

spark.stop()

#Create SparkSession for Classification Example

spark = SparkSession.builder.appName("Classification using SparkML").getOrCreate()
# read data
beans_data = spark.read.csv("drybeans.csv", header=True, inferSchema=True)
# Convert Class column from string to numerical values
indexer = StringIndexer(inputCol="Class", outputCol="label")
beans_data = indexer.fit(beans_data).transform(beans_data)
# Prepare feature vector
assembler = VectorAssembler(inputCols=["Area","Perimeter","Solidity","roundness","Compactness"], outputCol="features")
beans_transformed_data = assembler.transform(beans_data)
# Split data into training and testing sets
(training_data, testing_data) = beans_transformed_data.randomSplit([0.7, 0.3], seed=42)
# Create LR model for training on training set
lr = LogisticRegression(featuresCol="features", labelCol="label")
model = lr.fit(training_data)
# Make predictions on testing data
predictions = model.transform(testing_data)
# Evaluate model performance
evaluator = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="accuracy")
accuracy = evaluator.evaluate(predictions)
print("Accuracy =", accuracy)
# Calculate Precision
evaluator = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="weightedPrecision")
precision = evaluator.evaluate(predictions)
print("Precision =", precision)
# Calculate Recall
evaluator = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="weightedRecall")
recall = evaluator.evaluate(predictions)
print("Recall =", recall)
# Calculate F1 score
evaluator = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="f1")
f1_score = evaluator.evaluate(predictions)
print("F1 score = ", f1_score)

spark.stop()

#Create SparkSession for Clustering Example

spark = SparkSession.builder.appName("Clustering using SparkML").getOrCreate()
# Read data
# Load customers dataset
customer_data = spark.read.csv("customers.csv", header=True, inferSchema=True)
# Assemble the features into a single vector column
feature_cols = ['Fresh_Food', 'Milk', 'Grocery', 'Frozen_Food']
assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
customer_transformed_data = assembler.transform(customer_data)
number_of_clusters = 3
# Create K-Means Clustering Model
kmeans = KMeans(k = number_of_clusters)
#Train and Fit on DataSet
model = kmeans.fit(customer_transformed_data)
# Make predictions on the dataset
predictions = model.transform(customer_transformed_data)
predictions.groupBy('prediction').count().show()
#stop spark session
spark.stop()
