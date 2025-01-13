
def get_river_data(data, id):
    try:
        if isinstance(data, list):
            if not data:  # Check if the list is empty
                return None 
            for item in data:
                if item.get('id') == int(id):
                    return item.get('waterLevel', 'Water level not available')
            return None 
        else:
            return 'Invalid data format received.'  

    except Exception as error:
        return f"Error: {error}"  
