import pyspark
from pyspark.sql import SparkSession
import re 


spark = SparkSession.builder \
    .appName("UniqueWordCount") \
    .master("local[*]") \
    .getOrCreate()

sc = spark.sparkContext

text_rdd = sc.textFile("input.txt")


def clean_data_split(line):
    words = re.findall(r'\b[a-zA-Z]+\b', line.lower())
    return words


words_rdd = text_rdd.flatMap(clean_data_split)

unique_words_rdd = words_rdd.distinct()

count = unique_words_rdd.count()

print(f"Количество уникальных слов: {count}")

spark.stop()