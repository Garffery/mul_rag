try:
    from config import Mul_Agent_Config
    print("Import successful")
    print(Mul_Agent_Config)
except ImportError as e:
    print(f"Import failed: {e}")
except Exception as e:
    print(f"Error: {e}")
