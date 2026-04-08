from pydantic import BaseModel, ConfigDict
from typing import Optional

class LoanApplication(BaseModel):
    model_config = ConfigDict(extra='allow')
    
    Annual_Income: Optional[float] = None
    Monthly_Expenses: Optional[float] = None
    Dependents: Optional[int] = None
    FICO_Score: Optional[float] = None
    Debt_to_Income_Ratio: Optional[float] = None
    Credit_Utilization: Optional[float] = None
