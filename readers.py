from abc import ABC, abstractmethod
import base64
import io
import pandas as pd



class BaseDataStruct(ABC):

    @classmethod
    @abstractmethod
    def from_dataframe(cls, dataframe:pd.DataFrame) -> "BaseDataStruct":
        pass


    @classmethod
    @abstractmethod
    def from_dict(cls, data:dict) -> "BaseDataStruct":
        pass

    def __init__(self, x:list[float], y:list[float], z:list[float]):
        """
        Base class from which to construct data import types
        """
        self.x = x
        self.y = y
        self.z = z
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    
    def width(self) -> float:
        return max(self.x) - min(self.x)
    

    def height(self) -> float:
        return max(self.y) - min(self.y)
    
# --- End of BaseDataStruct ---


# Simplest implementation of data
class DataXYZ(BaseDataStruct):

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
        super().__init__(x, y, z)
    

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

# --- End of DataXYZ ---


def jaw():
    pass

def parse_contents(contents, filename) -> DataXYZ|None:
    content_type, content_string = contents.split(',')
    bytes = base64.b64decode(content_string)

    # Assume the user uploaded a CSV file
    if '.csv' in filename:
        df = pd.read_csv(io.StringIO(bytes.decode('utf-8')))
        return DataXYZ.from_dataframe(df)
    
    elif '.txt' in filename:
        df = pd.read_csv(io.StringIO(bytes.decode('utf-8')), delimiter='\t')
        return DataXYZ.from_dataframe(df)
    
    else:
        # File type NOT supported
        return None
    

