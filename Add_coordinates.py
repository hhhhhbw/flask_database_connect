import json
import pandas as pd

def read_geojson_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def read_excel_file(file_path):
    return pd.read_excel(file_path)

def create_province_coordinate_dict(geojson_data):
    province_coordinates = {}
    for feature in geojson_data['features']:
        province_name = feature['properties']['name']
        coordinates = feature['geometry']['coordinates']
        province_coordinates[province_name] = coordinates
    return province_coordinates

def add_coordinates_to_dataframe(df, province_coordinates):
    df['coordinates'] = None
    for index, row in df.iterrows():
        province_name = row['province_name']
        coordinates = province_coordinates.get(province_name, None)
        # 将找到的坐标作为列表存储在 DataFrame 中
        df.at[index, 'coordinates'] = coordinates
    return df

def save_dataframe_to_excel(df, file_path):
    # 使用 converter 将 coordinates 列转换为字符串，以便将其保存到 Excel 文件中
    df.to_excel(file_path, index=False, converters={'coordinates': str})

def main():
    geojson_data = read_geojson_file('world-eckert3-highres.geo.json')
    df = read_excel_file('description.xlsx')
    province_coordinates = create_province_coordinate_dict(geojson_data)
    df_with_coordinates = add_coordinates_to_dataframe(df, province_coordinates)
    save_dataframe_to_excel(df_with_coordinates, 'provinces_with_coordinates.xlsx')

if __name__ == '__main__':
    main()
