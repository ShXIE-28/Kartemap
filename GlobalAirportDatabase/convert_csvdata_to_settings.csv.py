import numpy as np
import pandas as pd

airport_file = 'GlobalAirportDatabase.csv'
metro_areas_file = 'metro_areas.csv'


def convert_csvdata():
    data_name = 'METRO AREAS'
    print('*' * len(data_name))
    print(data_name)
    print('*' * len(data_name))

    df = pd.read_csv(metro_areas_file)
    print(f'shape={df.shape}')

    print('keep only first 3 columns')
    idx = np.r_[3:len(df.columns)]
    df.drop(df.columns[idx], axis=1, inplace=True)

    print('keep only top 50 MSA, rows 1 to 50')
    df.drop(df.index[51:], inplace=True)
    print(f'updated shape={df.shape}')

    # after remove some strange characters
    # add column "City"
    df["City"] = df['Metropolitan_Statistical_Area'].apply(lambda x: x[:x.find("-")])
    
    print(df.head(20))
    df.to_csv("MetroAreas.csv")

    data_name = 'AIRPORT DATA'
    print('*' * len(data_name))
    print(data_name)
    print('*' * len(data_name))

    df1 = pd.read_csv(airport_file, sep=':', header=None)
    print(f'shape={df1.shape}')

    print('rename columns')
    df1.columns = ['CAO Code',
                   'Code',
                   'Name',
                   'City',
                   'Country',
                   'Latitude Degrees',
                   'Latitude Minutes',
                   'Latitude Seconds',
                   'Latitude Direction',
                   'Longitude Degrees',
                   'Longitude Minutes',
                   'Longitude Seconds',
                   'Longitude Direction',
                   'Altitude',
                   'Latitude',
                   'Longitude']

    print('keep only pertient columns [Code, Name, City. Country, Altitude, Latitude Longitudinal')
    idx = np.r_[0, 5:13]
    df1.drop(df1.columns[idx], axis=1, inplace=True)
    print(f'shape={df1.shape}')

    print('drop all non-USA airports')
    df1.drop(df1[df1.Country != 'USA'].index, inplace=True)
    print(f'shape={df1.shape}')

    print(df1.head(20))
    df1.to_csv("airport.csv")


if __name__ == '__main__':
    convert_csvdata()
