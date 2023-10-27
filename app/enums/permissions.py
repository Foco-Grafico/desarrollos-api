from enum import Enum

class ACCOUNT(Enum):
    CREATE = 'account.create'

class ROLE(Enum):
    CREATE = 'role.create'

class BATCH(Enum):
    CREATE = 'batch.create'
    DELETE = 'batch.delete'