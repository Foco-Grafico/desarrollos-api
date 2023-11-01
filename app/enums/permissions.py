from ast import Delete
from enum import Enum

class ACCOUNT(Enum):
    CREATE = 'account.create'

class DEVELOPMENT(Enum):
    CREATE = 'development.create'
    DELETE = 'development.delete'

class BATCH(Enum):
    CREATE = 'batch.create'
    DELETE = 'batch.delete'

class PAYMENT_PLAN(Enum):
    CREATE = 'paymentplan.create'

class ROLE(Enum):
    CREATE = 'role.create'
    DELETE = 'role.delete'
    UPDATE = 'role.update'
    
class SELLER(Enum):
    CREATE = 'seller.create'
    UPDATE = 'seller.update'
    DELETE = 'seller.delete'
    
