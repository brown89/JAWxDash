from dataclasses import dataclass
import base64
import io
import pandas as pd
import re
import numpy as np


@dataclass
class Settings:
    angle_of_incident:int = 65
    spot_size:float = 3.0
    colormap:str = 'viridis'
    sample_outline:str = None


    def to_dict(self) -> dict:
        return dict(
            angle_of_incident=self.angle_of_incident,
            spot_size=self.spot_size,
            colormap=self.colormap,
            sample_outline=self.sample_outline,
        )


class DataXYC:
    SCALE = 0.2  # Used for creating the zoom

    @classmethod
    def from_dict(cls, dict_data) -> "DataXYC":
        
        return DataXYC(
            data=pd.DataFrame(data=dict_data['data']),
            settings=dict_data['settings']
        )
    

    def __init__(self, data:pd.DataFrame, settings:Settings):
        """
        Base class from which to construct data import types
        """
        self.data = data
        self.settings = settings
        pass

    
    def width(self) -> float:
        return max(self.data.x) - min(self.data.x)
    

    def height(self) -> float:
        return max(self.data.y) - min(self.data.y)
    

    def normalized(self, column_id:str|int = 0) -> np.ndarray:
        # Needs work, but we'll start by accessing the first key in 'c'.

        if isinstance(column_id, str):
            c = self.data[column_id].to_numpy()
        elif isinstance(column_id, int):
            c = self.data.iloc[:, column_id].to_numpy()
        else:
            raise ValueError("column_id must be a string or integer")
        
        c = c - min(c)
        
        return c/max(c)
    

    def x_range(self) -> list:
        return [
            min(self.data.x) - DataXYC.SCALE*self.width(),  # min
            max(self.data.x) + DataXYC.SCALE*self.width()  # max
        ]
    
    def y_range(self) -> list:
        return [
            min(self.data.y) - DataXYC.SCALE*self.height(),  # min
            max(self.data.y) + DataXYC.SCALE*self.height()  # max
        ]
    
    def len(self) -> int:
        return len(self.data.index)
    
    def to_dict(self):

        return dict(
            data=self.data.to_dict(orient="list"),
            settings=self.settings.to_dict()
        )
# --- End of BaseDataStruct ---


def read_xyz_csv(file:bytes) -> pd.DataFrame:
    df = pd.read_csv(io.StringIO(file.decode("utf-8")))

    return df


def read_xyz_txt(file:bytes) -> pd.DataFrame:
    df = pd.read_csv(io.StringIO(file.decode('utf-8')), delimiter='\t')

    return df


def read_jaw_txt(file:bytes) -> pd.DataFrame:

    # Opening file and reading into list
    buffer = io.StringIO(file.decode("utf-8"))
    lines = buffer.readlines()
    

    # Find lines with the data, by matching (decimal,decimal)

    # Pattern explanation
    # \( and \): Match the parentheses that enclose the two numbers.
    # [+-]?: Matches an optional + or - sign before each number.
    # \d+\.\d+: Matches a decimal number (one or more digits before and after the decimal point).
    # ,: Matches the comma separating the two numbers.
    pattern = r"\([+-]?\d+\.\d+,[+-]?\d+\.\d+\)"

    data_line = False
    for i, line in enumerate(lines):
        matches = re.findall(pattern, line)
        if matches:
            data_line = i
            break
    

    # Reading the file with Pandas
    df = pd.read_csv(io.StringIO(file.decode("utf-8")), delimiter="\t", header=0, skiprows=range(1, data_line))
    

    # Renaming columns as to remove none ASCII char, replace white-space with underscore and set all lower caps
    def header_naming_scheme(dataframe:pd.DataFrame) -> pd.DataFrame:
        
        headers = {}
        for header in dataframe.columns:

            # Replacing white-space and setting to lower case
            new_header = header.replace(" ", "_").strip()

            # Removing non ASCII characters
            new_header = ''.join(c for c in new_header if ord(c) < 128)

            # Saving to 'headers'-dict
            headers[header] = new_header
            
        return dataframe.rename(headers)
    
    df = header_naming_scheme(df)
    

    # Extract x and y
    pattern = r"[+-]?\d+\.\d+"
    x, y = [], []
    for xy in df.iloc[:, 0].values.tolist():
        matches = re.findall(pattern, xy)

        if len(matches) == 2:
            x.append(float(matches[0]))
            y.append(float(matches[1]))
        
        else:
            x.append(np.nan)
            y.append(np.nan)

            print("Woopsie!")
            print(i, len(matches))

    # Adding x and y to DataFrame
    df['x'] = x
    df['y'] = y

    # Drops first (zero'th) column
    df = df.drop(columns=df.columns[0], axis=1)

    # Drop rows with NaN values
    df = df.dropna()
    
    return df


def parse_contents(contents, filename) -> DataXYC|None:
    content_type, content_string = contents.split(',')
    file = base64.b64decode(content_string)

    # Assume the user uploaded a CSV file
    if '.csv' in filename:
        data = read_xyz_csv(file)
        settings = Settings()

        return DataXYC(data, settings)
    
    elif '.txt' in filename:
        data = read_jaw_txt(file)
        settings = Settings()
        return DataXYC(data, settings)
    
    else:
        # File type NOT supported
        return None
    

