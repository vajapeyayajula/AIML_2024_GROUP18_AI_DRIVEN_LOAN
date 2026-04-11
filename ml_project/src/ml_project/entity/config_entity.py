from pydantic import BaseModel, ConfigDict
from typing import Optional

class LoanApplication(BaseModel):
    model_config = ConfigDict(extra='allow')
    
    # Personal & Demographic
    Age: Optional[int] = None
    Gender: Optional[str] = None
    Marital_Status: Optional[str] = None
    Education_Level: Optional[str] = None
    Dependents: Optional[int] = None
    
    # Employment
    Employment_Type: Optional[str] = None
    Years_at_Current_Job: Optional[int] = None
    Employer_Category: Optional[str] = None
    
    # Financials
    Annual_Income: Optional[float] = None
    Total_Assets: Optional[float] = None
    Monthly_Expenses: Optional[float] = None
    Savings_Balance: Optional[float] = None
    
    # Credit Profile
    FICO_Score: Optional[float] = None
    Debt_to_Income_Ratio: Optional[float] = None
    Credit_Utilization: Optional[float] = None
    Existing_Credits_Count: Optional[int] = None
    Prev_Defaults: Optional[int] = None
    
    # Loan Details
    Loan_Amount: Optional[float] = None
    Loan_Purpose: Optional[str] = None
    Term_Months: Optional[int] = None
    Interest_Rate: Optional[float] = None
    Loan_to_Income_Ratio: Optional[float] = None
