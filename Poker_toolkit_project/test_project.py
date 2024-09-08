import pytest
from datetime import datetime
from project import PokerBankrollManager

def test_record_session():
    
    manager = PokerBankrollManager()
    
    manager.record_session(datetime(2024, 8, 30, 14, 0), datetime(2024, 8, 30, 17, 0), 100)
    
    
    assert len(manager.sessions) == 1
    assert manager.sessions[0]['profit_loss'] == 100
    assert manager.sessions[0]['duration'] == 3  

def test_generate_report():
    
    manager = PokerBankrollManager()
    
    manager.record_session(datetime(2024, 8, 30, 14, 0), datetime(2024, 8, 30, 17, 0), 100)
    manager.record_session(datetime(2024, 8, 31, 19, 0), datetime(2024, 8, 31, 23, 0), -50)
    
   
    try:
        manager.generate_report()
        assert True  
    except Exception:
        assert False  

def test_suggest_strategy():
    
    manager = PokerBankrollManager()
   
    manager.record_session(datetime(2024, 8, 30, 14, 0), datetime(2024, 8, 30, 17, 0), 100)
    manager.record_session(datetime(2024, 8, 31, 19, 0), datetime(2024, 8, 31, 23, 0), -1100)
    
    
    suggestion = manager.suggest_strategy()
    assert suggestion == "Consider reducing stakes to minimize losses."  # A javaslat helyes, mivel a veszteség nagy

if __name__ == "__main__":
    pytest.main()
