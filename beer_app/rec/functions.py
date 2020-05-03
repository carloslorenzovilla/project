# beer_app/rec/functions.py
from beer_app.models import Item, Location, Log
from beer_app.rec.rec_engine.functions import Rec_Engine
from numpy import where

class Get_Rec():

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
        self.rec_list = self.generate_rec()
    
    #So far, this will only print the available beers in a location and return them as recommendations
    #I need to figure out categories before we can make a recommendaiton.
    # category_id is the top recommendation category, therefore the engine selects a beer from the
    # location according to the category. We still need to add this category Column to the model and 
    # organize the syles into these specific groups.
    
    #returns 2D array, ([style, affinity])
    def generate_rec(self):
        affinity_vector = self.engine.affinity_vector
        # use the affinity vector to determine the top category, find the maximum value from the second column
        index = list(where(max(affinity_vector[1,:])))[0]
        
        category_id = int(affinity_vector[0,index[0]])
        # yields a number

        # print(self.zone_id)
        
        # if self.zone_id:
        #     location_id_list = [
        #                                     location.id
        #                                     for location
        #                                     in Location.query.filter_by(zone_id=self.zone_id)
        #                                  ]
        # else:
        location_id_list = [self.location_id]
        
        #return a list of lists of items filtered by location and top category
        rec_list = [
                            [
                                item.id
                                for item
                                in Item.query.filter_by(location_id=location_id)
                            ]
                            for location_id
                            in location_id_list
                        ]

        return rec_list[0]
       
    
