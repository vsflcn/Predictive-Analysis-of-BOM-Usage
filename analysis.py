import pandas as pd
import numpy as np
import sqlite3

df = pd.read_sql_query('SELECT * FROM inventory_usage', con=sqlite3.connect('inventory_data.sqlite'))

