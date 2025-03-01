import pandas as pd
import sqlite3

df = pd.read_sql_query('SELECT * FROM inventory_usage', con=sqlite3.connect('inventory_data.sqlite'))

class Bom_Usage:
    def __init__(self, data):
        self.data = data

    def material_usage_per_order(self):
        grouped_df = self.data.groupby(['product_identifier', 'semiproduct_index'])
        for (product_identifier, semiproduct_index), group in grouped_df:
            print(f"Processing Product: {product_identifier} | Semiproduct: {semiproduct_index}")

        for _, row in group.iterrows():
            print(f"{row['product_identifier']} | {semiproduct_index} | {row['order_number']} | "
                f"{row['material_index']} | {row['quantity']} | {row['unit']}")
           

    def semiproducts_ideal_bom_calculation(self):
        grouped_df = self.data.groupby(['product_identifier', 'semiproduct_index'])

        for (product_identifier, semiproduct_index), group in grouped_df:
            print(f"Processing Product: {product_identifier} | Semiproduct: {semiproduct_index}")

            aggregated = group.groupby('material_index')['quantity'].agg(
                total_quantity='sum',
                average_quantity='mean',
                std_quantity='std',
            ).reset_index()

            aggregated = aggregated.merge(
                    group[['material_index', 'unit']].drop_duplicates(),
                    on='material_index',
                    how='left'
                )
            
            for _, agg_row in aggregated.iterrows():
                ideal_quantity = agg_row['average_quantity']
                if not pd.isna(agg_row['std_quantity']):
                    ideal_quantity += agg_row['std_quantity']

                print(f"Material: {agg_row['material_index']} | Total Quantity: {agg_row['total_quantity']} | "
                      f"Average Quantity: {agg_row['average_quantity']} | Std Dev: {agg_row['std_quantity']} | "
                      f"Ideal Quantity: {ideal_quantity} | Unit: {agg_row['unit']}")
            
            print("-" * 150)

        return None
class Bom_Prediction:
    def __init__(self, df):
        self.data = df

    def usage_2023(self):
        grouped_df = self.data[self.data['production_year'] == 2023]

        for semiproduct_index, group in grouped_df.groupby('semiproduct_index'):
            aggregated = group.groupby('material_index')['quantity'].agg(
                total_quantity='sum',
                average_quantity='mean',
                std_quantity='std',
            ).reset_index()
            
            aggregated = aggregated.merge(
                    group[['material_index', 'unit']].drop_duplicates(),
                    on='material_index',
                    how='left'
                )
            
            for _, agg_row in aggregated.iterrows():
                ideal_quantity_2023 = agg_row['average_quantity']
                if not pd.isna(agg_row['std_quantity']):
                    ideal_quantity_2023 += agg_row['std_quantity']

                print(f"Material usage in 2023 for {semiproduct_index}: "
                      f"{agg_row['material_index']} | Total: {agg_row['total_quantity']} | "
                      f"Average: {agg_row['average_quantity']} | Std Dev: {agg_row['std_quantity']} | "
                      f"Ideal Quantity: {ideal_quantity_2023} | Unit: {agg_row['unit']}")
            
            print("-" * 150)
        
        return None 
    
    def usage_2024(self):
        grouped_df = self.data[self.data['production_year'] == 2024]

        for semiproduct_index, group in grouped_df.groupby('semiproduct_index'):
            aggregated = group.groupby('material_index')['quantity'].agg(
                total_quantity='sum',
                average_quantity='mean',
                std_quantity='std',
            ).reset_index()
            
            aggregated = aggregated.merge(
                    group[['material_index', 'unit']].drop_duplicates(),
                    on='material_index',
                    how='left'
                )
            
            for _, agg_row in aggregated.iterrows():
                ideal_quantity_2024 = agg_row['average_quantity']
                if not pd.isna(agg_row['std_quantity']):
                    ideal_quantity_2024 += agg_row['std_quantity']

                print(f"Material usage in 2023 for {semiproduct_index}: "
                      f"{agg_row['material_index']} | Total: {agg_row['total_quantity']} | "
                      f"Average: {agg_row['average_quantity']} | Std Dev: {agg_row['std_quantity']} | "
                      f"Ideal Quantity: {ideal_quantity_2024} | Unit: {agg_row['unit']}")
            
            print("-" * 150)
        
        return None  
    
    #def bom_usage_comparison_by_year(self):

        #return None


bom_prediction = Bom_Usage(df)


