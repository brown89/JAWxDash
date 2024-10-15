from abc import ABC, abstractmethod
import base64
import io
import pandas as pd
import re
import numpy as np


class DataXYC:

    @classmethod
    def from_dict(cls, data:dict) -> "DataXYC":

        return DataXYC(
            data['x'],
            data['y'],
            data['c'],
        )
    
    def __init__(self, x:list[float], y:list[float], c:dict):
        """
        Base class from which to construct data import types
        """
        self.x = x
        self.y = y
        self.c = c
        pass

    
    def width(self) -> float:
        return max(self.x) - min(self.x)
    

    def height(self) -> float:
        return max(self.y) - min(self.y)
    

    def z_normalized(self) -> list:
        # Needs work, but we'll start by accessing the first key in 'c'.

        key0 = list(self.c)[0]
        z_min, z_max = min(self.c[key0]), max(self.c[key0])
        diff = z_max - z_min
        return [(z - z_min) / diff for z in self.c[key0]]

    def to_dict(self) -> dict:
        return dict(
            x = self.x,
            y = self.y,
            c = self.c,
        )
# --- End of BaseDataStruct ---


def read_xyz_csv(file:bytes) -> DataXYC:
    df = pd.read_csv(io.StringIO(file.decode("utf-8")))

    return DataXYC(df.x, df.y, {"z": df.z})


def read_xyz_txt(file:bytes) -> DataXYC:
    df = pd.read_csv(io.StringIO(file.decode('utf-8')), delimiter='\t')

    return DataXYC(df.x, df.y, {'z': df.z})


def read_jaw_txt(file:bytes) -> DataXYC:

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
    
    df = df.drop(columns=df.columns[0], axis=1)

    # Converting datafram to dictionary
    c = {}
    for col in df.columns:
        c[col] = df[col].to_list()
    

    return DataXYC(x, y, c)


def parse_contents(contents, filename) -> DataXYC|None:
    content_type, content_string = contents.split(',')
    file = base64.b64decode(content_string)

    # Assume the user uploaded a CSV file
    if '.csv' in filename:
        return read_xyz_csv(file)
    
    elif '.txt' in filename:
        return read_jaw_txt(file)
    
    else:
        # File type NOT supported
        return None
    

