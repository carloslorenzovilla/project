# beer_app/rec/functions.py
from beer_app.models import Item, Location, Log
from beer_app.rec.rec_engine.functions import Rec_Engine

class Rec():

    def __init__(self, user_id, location_id=None, zone_id=None):
        self.user_id = user_id
        self.zone_id = zone_id
        self.location_id = location_id
        self.user_data =  [
                                        item.item_id 
                                        for item 
                                        in Log.query.filter_by(
                                            user_id=self.user_id).order_by(
                                            Log.date.desc()
                                        )
                                    ]
        self.engine = Rec_Engine(user_data=self.user_data)
    
    #returns 2D array, ([style, affinity])
    def generate_rec(self):
        affinity_vector = self.engine.affinity_vector()
        # use the affinity vector to determine the top category, find the maximum value from the second column
        category_id = max(affinity_vector([:,1]))
        # yields a number
        
        if self.zone_id:
            location_id_list = [
                                            location.id
                                            for location
                                            in Location.query.filter_by(zone_id=self.zone_id)
                                         ]
        else:
            location_id_list = [self.location_id]
        
        #return a list of lists of items filtered by location and top category
        return rec_list = [
                                        [
                                            item 
                                            for item 
                                            in Item.query.filter_by(location_id=location_id,category_id=category_id)
                                        ] 
                                        for location_id 
                                        in location_id_list
                                    ]
       
    
