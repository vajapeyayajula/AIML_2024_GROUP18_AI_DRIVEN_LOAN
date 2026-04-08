def test_ping(test_app):
    response = test_app.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}

def test_process_loan_applications(test_app):
    payload = [
        {
            "Annual_Income": 50000,
            "Monthly_Expenses": 2000,
            "Dependents": 2,
            "FICO_Score": 750,
            "Debt_to_Income_Ratio": 0.3,
            "Credit_Utilization": 0.2
        }
    ]
    response = test_app.post("/process_loan_applications", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["processed_count"] == 1
    assert "results" in response.json()
