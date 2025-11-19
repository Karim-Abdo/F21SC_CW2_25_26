def test_imports():
    print("\nTesting Python imports...")
    try:
        from analytics_manager import AnalyticsManager
        from data.data_loader import DataLoader  
        print("All imports successful")
        return True
    except ImportError as e:
        print(f"Import error: {e}")
        return False