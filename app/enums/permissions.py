from enum import Enum

class ACCOUNT(Enum):
    CREATE = 'account.create'

class DEVELOPMENT(Enum):
    CREATE = 'development.create'

class BATCH(Enum):
    CREATE = 'batch.create'
    DELETE = 'batch.delete'

class PAYMENT_PLAN(Enum):
    CREATE = 'paymentplan.create'

class ROLE(Enum):
    CREATE = 'role.create'
    DELETE = 'role.delete'