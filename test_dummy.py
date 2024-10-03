class Parent:
    def __init__(self, last_name:str='Stark'):
        self.last_name = last_name
    
    def to_dict(self):
        return {'last_name': self.last_name}


class Child(Parent):
    def __init__(self, name:str='Tony'):

        self.name = name
        super().__init__()
    

    def to_dict(self):
        return {
            'name': self.name,
            'last_name': super().to_dict(),
        }


a = Child()
print(a.to_dict())
