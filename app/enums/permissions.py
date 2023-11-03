from enum import Enum

class ACCOUNT(Enum):
    CREATE = 'account.create'
    ADD_PERMISSION = 'account.add_permission'

class DEVELOPMENT(Enum):
    CREATE = 'development.create'
    DELETE = 'development.delete'
    MODIFY = 'development.modify'

class BATCH(Enum):
    CREATE = 'batch.create'
    DELETE = 'batch.delete'
    MODIFY = 'batch.modify'

class PAYMENT_PLAN(Enum):
    CREATE = 'paymentplan.create'

class ROLE(Enum):
    CREATE = 'role.create'
    DELETE = 'role.delete'
    UPDATE = 'role.update'
    
class SELLER(Enum):
    CREATE = 'seller.create'
    UPDATE = 'seller.update'
    
