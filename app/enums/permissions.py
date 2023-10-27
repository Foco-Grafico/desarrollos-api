from enum import Enum

class ACCOUNT(Enum):
    CREATE = 'account.create'

class DEVELOPMENT(Enum):
    CREATE = 'development.create'

class BATCH(Enum):
    CREATE = 'batch.create'
    DELETE = 'batch.delete'

class PAYMENTPLAN(Enum):
    CREATE = 'paymentplan.create'
