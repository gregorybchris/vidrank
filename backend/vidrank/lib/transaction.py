from pydantic import BaseModel

from vidrank.lib.selection import Selection
from vidrank.lib.transaction_type import TransactionType


class Transaction(BaseModel):
    transaction_type: TransactionType
    selection: Selection
