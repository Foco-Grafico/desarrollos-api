from enum import Enum

class ACCOUNT(Enum):
    CREATE = 'account.create'

class ROLE(Enum):
    CREATE = 'role.create'

class SELLER(Enum):
    CREATE = 'seller.create'
    UPDATE = 'seller.update'
