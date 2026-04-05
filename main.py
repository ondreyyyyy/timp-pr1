from data_access import DataAccessLayer
from business_logic import BusinessLogicLayer
from presentation import PresentationLayer

def main():
    dal = DataAccessLayer()
    bl = BusinessLogicLayer(dal)
    ui = PresentationLayer(bl)
    
    ui.run()

if __name__ == "__main__":
    main()