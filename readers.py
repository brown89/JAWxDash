from abc import ABC
import base64
import io
import pandas as pd



class BaseDataStruct(ABC):

    def __init__(self, title:str, x:list[float], y:list[float], data:dict):
        """
        Base class from which to construct data import types
        """
        pass


# Simplest implementation of data
class DataXYZ:

    @classmethod
    def from_dataframe(cls, data_frame:pd.DataFrame):
        return DataXYZ(
            data_frame['x'].to_list(),
            data_frame['y'].to_list(),
            data_frame['z'].to_list()
        )
    

    @classmethod
    def from_dict(cls, data_xyz:dict) -> "DataXYZ":
        return DataXYZ(
            data_xyz['x'],
            data_xyz['y'],
            data_xyz['z']
        )
    
    
    def __init__(self, x:list[float], y:list[float], z:list[float]) -> None:
        self.x = x
        self.y = y
        self.z = z
    
    def to_dict(self):
        return {
            'x': self.x,
            'y': self.y,
            'z': self.z,
        }
    
    def z_normalized(self) -> list:
        z_baseline = [z - min(self.z) for z in self.z]
        z_max = max(z_baseline)
        return [z/z_max for z in z_baseline]
    

    def width(self) -> float:
        return max(self.x) - min(self.x)
    

    def height(self) -> float:
        return max(self.y) - min(self.y)
    


def parse_contents(contents, filename) -> DataXYZ|None:
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    # Assume the user uploaded a CSV file
    if '.csv' in filename:
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        return DataXYZ.from_dataframe(df)
    
    elif '.txt' in filename:
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), delimiter='\t')
        return DataXYZ.from_dataframe(df)
    
    else:
        # File type NOT supported
        return None
    

