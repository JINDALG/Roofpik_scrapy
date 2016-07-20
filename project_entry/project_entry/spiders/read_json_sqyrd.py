unit = {
      "configurations": {
        "propertyType": "",
        "type": "",
        "price": {"booking":{"min":0,"max":0},
          "resale":{"min":0,"max":0}  
        },
        "superArea": "",
        "carpetArea": "",
        "totalBalconies": "",
        "kitchen": "",
        "pujaRoom": "",
        "storeRoom": "",
        "totalHalls": "",
        "studyRoom": "",
        "familyLounge": "",
        "totalBedrooms": "",
        "totalWashrooms": "",
        "servantRoom": ""
      },
      "specifications": {
        "showerCubicle": "",
        "homeAutomation": "",
        "vrvAirConditioning": "",
        "kitchenAppliances": "",
        "kitchenOTG": "",
        "bathTub": "",
        "kitchenModular": "",
        "kitchenDishWasher": "",
        "airConditioning": "",
        "flooringMasterBedrooms": "",
        "kitchenChimney": "",
        "flooringLivingDining": "",
        "kitchenMicrowaveOven": "",
        "jacuzzi": "",
        "kitchenRefrigerator": "",
        "flooringOtherBedrooms": "",
        "kitchenHob": "",
        "fullyFurnished": "",
        "wardrobes": ""
      }
    }

import json
from pprint import pprint
import copy
import os
def convert(mydata):
    # with open("square_yard.json") as json_file:
    #     mydata = json.load(json_file)

    with open(os.path.dirname(__file__)+"/roofpik_obj.json") as json_file:
        firebase_data = json.load(json_file)

    try :
        firebase_data['projectDetails']['address']['address_line1'] = mydata['address']
    except :
        pass
    try :
        firebase_data['areas']['max'] = mydata['max_area']
    except :
        pass
    try :
        firebase_data['areas']['min'] = mydata['min_area']
    except :
        pass
    try :
        firebase_data['areas']['pricePerSquareFeet'] = mydata['price_per_sqft']
    except :
        pass
    try :
        firebase_data['projectDetails']['projectName'] = mydata['name']
    except :
        pass
    try :
        firebase_data['projectStatus'] = mydata['possession_status']
    except :
        pass
    try :
        firebase_data['priceRange']['buy']['booking']['max'] = mydata['max_price']
    except :
        pass
    try :
        firebase_data['priceRange']['buy']['booking']['min'] = mydata['min_price']
    except :
        pass
    


    try :
        firebase_data['other']['powerBackup'] = mydata['amenities']['Convenience']['Power Backup']
    except :
        pass
    try :
        firebase_data['other']['laundry'] = mydata['amenities']['Convenience']['Laundromat']
    except :
        pass
    try :
        firebase_data['other']['airConditioningInWaitingLounge'] =  mydata['amenities']['Convenience']['AC Waiting Lobby']
    except :
        pass
    try :
        firebase_data['other']['daycare'] =mydata['amenities']['Convenience']['Day Care Center']
    except :
        pass
    try :
        firebase_data['other']['petFriendly'] = mydata['amenities']['Convienice']['Pet Area']
    except :
        pass
    try :
        firebase_data['other']['playSchool'] = mydata['amenities']['Convience']['Pre-School']
    except :
        pass
    try :
        firebase_data['other']['park'] = mydata['amenities']['Environment']['Normal Park OR Central Green']
    except :
        pass
    try :
        firebase_data['other']['pharmacy'] = mydata['amenities']['Convience']['Medical Facility']
    except :
        pass
    try :
        firebase_data['other']['waitingLoungeInTower'] = mydata['amenities']['Convience']['AC Waiting Lobby']
    except :
        pass
    try :
        firebase_data['other']['grocery'] = mydata['amenities']['Convience']['Attached Market']
    except :
        pass

    try :
        firebase_data['clubHouse']['danceRoom']= mydata['Leisure']['Dance Room']
        firebase_data['clubHouse']['spa'] = mydata['Leisure']['Spa']
        firebase_data['clubHouse']['miniTheatre'] = mydata['Leisure']['Mini Theatre'] 
        firebase_data['clubHouse']['jacuzzi'] = mydata['Leisure']['Jacuzzi'] 
        firebase_data['clubHouse']['saunaRoom'] = mydata['Leisure']['Sauna']
        firebase_data['clubHouse']['cafe'] = mydata['Leisure']['Cafe OR Coffee Bar'] 
            

        firebase_data['sportsActivities']['badminton'] = mydata['Sports']['Badminton Court(s)']
        firebase_data['sportsActivities']['cricket'] = mydata['Sports']['Cricket'] 
        firebase_data['sportsActivities']['football'] = mydata['Sports']['Football']
        firebase_data['sportsActivities']['joggingTrack'] = mydata['Sports']['Jogging OR Cycle Track'] 
        firebase_data['sportsActivities']['amphitheatre'] =  mydata['Leisure']['Amphitheater']
        firebase_data['sportsActivities']['tennis'] = mydata['Sports']['Tennis Court(s)']
        firebase_data['sportsActivities']['swimmingPool'] =mydata['Sports']['Swimming Pool'] 
        firebase_data['sportsActivities']['kidsSwimmingPool'] = mydata['Sports']['Kids Pool']
        firebase_data['sportsActivities']['skatingRink'] = mydata['Sports']['Skating Rink'] 
        firebase_data['sportsActivities']['squash'] = mydata['Sports']['Squash Court'] 
        firebase_data['sportsActivities']['tableTennis'] =  mydata['Sports']['Table Tennis'] 
        firebase_data['sportsActivities']['basketball'] = mydata['Sports']['Basketball'] 
        firebase_data['sportsActivities']['volleyball'] = mydata['Sports']['Volleyball'] 
        firebase_data['sportsActivities']['snookerTable'] = mydata['Sports']['SnookerORPoolORBilliards']
        firebase_data['sportsActivities']['bowlingAlley'] = mydata['Leisure']['Bowling'] 

        firebase_data['security']['videoDoorPhone'] = mydata['Safety']['Video Phone'] 
        firebase_data['security']['mainGate']['cctv'] = mydata['Safety']['CCTV / Video Surveillance'] 
        firebase_data['security']['mainGate']['guard'] = mydata['Safety']['24 x 7 Security'] 
    except :
        pass

    for key in mydata['connecting_road']:
        try :
            if "Express" in key:
                firebase_data['connectivity']['nearestExpressway'] = key
                firebase_data['connectivity']['expresswayDistance'] = mydata['connecting_road'][key]
            else :
                firebase_data['connectivity']['nearestMainRoad'] = key
                firebase_data['connectivity']['mainRoadDistance'] = mydata['connecting_road'][key]
        except :
            pass

    i = 1
    for bhk in mydata['more_info']:
        for entry in mydata['more_info'][bhk]:
            try :
                temp = copy.deepcopy(unit)
                temp['configurations']['propertyType'] = mydata.get('projectType',None)
                temp['configurations']['type'] = bhk.split('-')[0]
                temp['configurations']['price']['booking']['min'] = entry.get('min_price',None)
                temp['configurations']['price']['booking']['max'] = entry.get('max_price',None)
                temp['configurations']['superArea'] = entry.get('built_up_area',None)
                temp['configurations']['carpetArea'] = entry.get('carpet_area',None)
                temp['configurations']['servantRoom'] = entry.get('servent_room',None)
                temp['configurations']['kitchen'] = entry.get('kitchen',None)
                try :
                    temp['configurations']['totalBalconies'] = entry['balconies']['count']
                except :
                    pass
                temp['configurations']['totalBedrooms'] = entry.get('bedrooms',None)
                temp['configurations']['totalWashrooms'] = entry.get('bathrooms',None)

                firebase_data['units']['id'+str(i)] = copy.deepcopy(temp)
                i+=1
            except :
                import traceback
                print traceback.print_exc()
                input()

    pprint(firebase_data['units'])

    try :
        if 'apartment' in mydata['property_type'].lower():
            firebase_data['projectDetails']['projectType']['apartment'] =  True
        if 'villa' in mydata['property_type'].lower():
            firebase_data['projectDetails']['projectType']['villa'] =  True
    except :
        pass
    # pprint(firebase_data)
    return firebase_data