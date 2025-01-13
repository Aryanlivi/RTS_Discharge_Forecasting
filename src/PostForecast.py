from River import River
from dotenv import load_dotenv
from Utils import get_river_data
import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Socket.ApiService import APIService
from DB_Service.Database import Database


load_dotenv()
#ENV CONSTANTS:
GALCHI_TABLE=os.getenv('galchi_table')
BUDHI_TABLE=os.getenv('budhi_table')
SIURENITAR_TABLE=os.getenv('siurenitar_table')




def compute_and_post(data):
    #Initializing:
    # SocketGalchiId=os.getenv('SocketGalchiId')
    # SocketBudhiId=os.getenv('SocketBudhiId')
    # galchi_data=get_river_data(data=data,id=SocketGalchiId)
    # budhi_data=get_river_data(data=data,id=SocketBudhiId)
    
    ##FOR TESTS:
    galchi_data={'datetime': '2025-01-13T08:55:00+00:00', 'value': 366.051483154}
    budhi_data={'datetime': '2025-01-13T08:55:00+00:00', 'value': 333.470916748}
    
    if not galchi_data or not budhi_data: 
        return

    #Create River Obj:
    galchi=River('Galchi',galchi_data['datetime'],galchi_data['value'])
    budhi=River('Budhi',budhi_data['datetime'],budhi_data['value'])
    
    galchi.compute_forecast()
    budhi.compute_forecast()  
    print(f"Original galchi data:{galchi.get_data()}")
    print(f"Original budhi data:{budhi.get_data()}")

    print("---------------------------")
    
    
    print(f"Galchi Forecasted:{galchi.get_forecasted_data()}")
    print(f"Budhi Forecasted:{budhi.get_forecasted_data()}")
    print('-------------------------------------------')
    db=Database()
    db.connect()
    db.insert_data(GALCHI_TABLE,galchi.get_forecasted_data())
    db.insert_data(BUDHI_TABLE,budhi.get_forecasted_data())
    db.disconnect()
    
compute_and_post({})