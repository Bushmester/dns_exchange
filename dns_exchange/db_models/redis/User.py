from dns_exchange.dictionaries import db


class User:
    __slots__ = ('id', 'name', 'surname')
    __table_name = 'users'

    # Create method
    def __new__(cls, user_id, name, surname, *args, **kwargs):
        instance = super().__new__(cls, *args, **kwargs)
        if cls.__table_name not in db:
            db[cls.__table_name] = []
        db[cls.__table_name].append({'id': user_id, 'name': name, 'surname': surname})
        return instance

    # Update method
    def __setattr__(self, item, value):
        super().__setattr__(item, value)
        list(filter(lambda x: x['id'] == self.id, db[self.__table_name]))[0][item] = value

    # Retrieve method
    @classmethod
    def retrieve(cls, **kwargs):
        return cls.list(**kwargs)[0]

    # List method
    @classmethod
    def list(cls, **kwargs):
        def filter_func(obj):
            for kwarg in kwargs.items():
                if not obj[kwarg[0]] == kwarg[1]:
                    return False
            return True
        return list(filter(filter_func, db[cls.__table_name]))

    # Delete method
    def __del__(self):
        del db[self.__table_name][db[self.__table_name].index(list(filter(lambda x: x['id'] == self.id, db[self.__table_name]))[0])]

    def __init__(self, user_id: int, name: str, surname: str):
        self.id = user_id
        self.name = name
        self.surname = surname


user0 = User(0, 'Ilnar', 'Gomelyanov')
user1 = User(1, 'Rustem', 'Saitgareev')
user2 = User(2, 'Rustem', 'Gomelyanov')
print(f'(create test) init, DB:\n{db}\n')

user0.name = 'notIlnar'
print(f'(update test) Ilnar => notIlnar, DB:\n{db}\n')

user = User.list(id=2)
print(f'(retrieve test) id=2, user:\n{user}\n')

users = User.list(name='Rustem')
print(f'(list test) name=Rustem, users:\n{users}\n')

del user0
print(f'(delete test) delete notIlnar, DB:\n{db}\n')

