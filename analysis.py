import pandas as pd
import numpy as np
import sqlite3
import statistics

df = pd.read_sql_table('inventory_data.sqlite', con = sqlite3.connect('inventory_data.sqlite'))
