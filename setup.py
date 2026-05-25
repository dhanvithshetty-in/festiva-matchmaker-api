from data.generate_vendors import generate_mock_data
from models.ranking_model import VendorRanker

if __name__ == "__main__":
    generate_mock_data()
    VendorRanker().train()
    print("🎯 System setup complete.")