import pandas as pd
import numpy as np

# import data files
cell_data = pd.read_csv('ParameterData_Main.txt', sep='\t')
mito_data = pd.read_csv('ParameterData_mito.txt', sep='\t')

# remove cells and mito out of gate
cell_data = cell_data[cell_data['Cells'] == 1].reset_index(drop=True)
mito_data = mito_data[mito_data['MO.Cells'] == 1].reset_index(drop=True)

"""(1) How many mitochondria there are on average (and the standard deviation) per cell in each well"""

# count mito per cell
mito_count = mito_data['Parent Object ID (MO)'].value_counts().to_frame()
mito_count = mito_count.rename({'Parent Object ID (MO)':'mito count per cell'}, axis='columns')
# change index in mito_count into cell index, instead of cell ID
mito_count['index'] = np.nan  # add empty (nan) column to mito_count dataframe (to be filled later)
for i in mito_count.index:
    mito_count.loc[i, 'index'] = cell_data.index[cell_data['Object ID'] == i].tolist()[0]
mito_count['index'] = mito_count['index'].apply(np.int64)
mito_count = mito_count.set_index('index')
# add mito count column to cell_data dataframe
cell_data['mito count'] = mito_count
cell_data['mito count'] = cell_data['mito count'].fillna(0) # turn nan values into 0
cell_data['mito count'] = cell_data['mito count'].apply(np.int64)
# save mito_count as csv file
mito_count['Cell ID'] = mito_count.index
mito_count[['Cell ID', 'mito count per cell']].to_csv('mito per cell count.csv', index=False)

# calc mean and std of mito per cell in each well
mito_per_cell_data = pd.DataFrame()
mito_per_cell_data['Well'] = pd.unique(cell_data['Well '])  # add Well column to mito_per_cell dataframe
# add empty (nan) columns to mito_per_cell dataframe (to be filled later)
mito_per_cell_data['Mean'] = np.nan
mito_per_cell_data['STD'] = np.nan
for w in mito_per_cell_data['Well']:
    mito_per_cell_data.loc[mito_per_cell_data['Well'] == w, 'Mean'] = cell_data[cell_data['Well '] == w]['mito count'].mean()
    mito_per_cell_data.loc[mito_per_cell_data['Well'] == w, 'STD'] = cell_data[cell_data['Well '] == w]['mito count'].std()
# save mito_count as csv file
mito_per_cell_data.to_csv('mito per cell mean and std.csv', index=False)

"""(2) What is the average (and SD) of the circularity, intensity and area of mitochondria per well."""
mito_per_well_data = pd.DataFrame()
mito_per_well_data['Well'] = pd.unique(cell_data['Well '])
# add empty (nan) columns to mito_per_well dataframe (to be filled later)
mito_per_well_data['Mean Circularity'] = np.nan
mito_per_well_data['STD Circularity'] = np.nan
mito_per_well_data['Mean Area'] = np.nan
mito_per_well_data['STD Area'] = np.nan
mito_per_well_data['Mean Intensity'] = np.nan
mito_per_well_data['STD Intensity'] = np.nan
for w1 in mito_per_well_data['Well']:
    mito_per_well_data.loc[mito_per_well_data['Well'] == w1, 'Mean Circularity'] = mito_data[mito_data['Well '] == w1]['Circularity '].mean()
    mito_per_well_data.loc[mito_per_well_data['Well'] == w1, 'STD Circularity'] = mito_data[mito_data['Well '] == w1]['Circularity '].std()
    mito_per_well_data.loc[mito_per_well_data['Well'] == w1, 'Mean Area'] = mito_data[mito_data['Well '] == w1]['Area '].mean()
    mito_per_well_data.loc[mito_per_well_data['Well'] == w1, 'STD Area'] = mito_data[mito_data['Well '] == w1]['Area '].std()
    mito_per_well_data.loc[mito_per_well_data['Well'] == w1, 'Mean Intensity'] = mito_data[mito_data['Well '] == w1]['Mean Intensity TransCon'].mean()
    mito_per_well_data.loc[mito_per_well_data['Well'] == w1, 'STD Intensity'] = mito_data[mito_data['Well '] == w1]['Mean Intensity TransCon'].std()
# save mito_count as csv file
mito_per_well_data.to_csv('mito per well area circularity and intensity mean and std.csv', index=False)
