import redis
from redisgraph import Graph
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Connect to Redis
redis_con = redis.Redis()
graph = Graph('game', redis_con)

# Define the players and strategies
players = ['Alice', 'Bob']
strategies = ['Cooperate', 'Defect']

# Create the graph
graph.query("CREATE (:Root {name: 'Game'})")
for player in players:
    graph.query(f"MATCH (r:Root) CREATE (r)-[:HAS_PLAYER]->(:Player {{name: '{player}'}})")
for strategy in strategies:
    graph.query(f"MATCH (r:Root) CREATE (r)-[:HAS_STRATEGY]->(:Strategy {{name: '{strategy}'}})")

# Create a 2D array to store random data
data = np.random.rand(len(players), len(strategies))

# Create a dataframe to use with Seaborn
df = pd.DataFrame(data, index=players, columns=strategies)

# Store the random data in RedisGraph nodes
for i, player in enumerate(players):
    for j, strategy in enumerate(strategies):
        value = data[i][j]
        node = graph.query(f"MATCH (p:Player {{name: '{player}'}})-[:HAS_STRATEGY {{name: '{strategy}'}}]->(s:Strategy) RETURN s")[0][0]
        graph.query(f"MATCH (p:Player {{name: '{player}'}}), (s:Strategy {{name: '{strategy}'}}) CREATE (p)-[:USES {{value: {value}}}]->(s)")

# Create the heatmap
sns.heatmap(df, cmap='YlGnBu')

# Show the plot
plt.show()
