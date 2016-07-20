    
import json
from pprint import pprint
import os
import copy
# with open("data.json") as json_file:
#     my_data = json.load(json_file)
    

# #print firebase_data
# with open("obj.json",'w') as json_file:
#     json_file.write(json.dumps(firebase_data))



def convert(my_data):
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
    with open(os.path.dirname(__file__)+"/roofpik_obj.json") as json_file:
        firebase_data = json.load(json_file)
    my_data['amenity'] = ' '.join(my_data['amenity']).lower()

    firebase_data['projectStatus'] = my_data['status']
    firebase_data['priceRange']['buy']['booking']['min'] = my_data['min_booking_price']
    firebase_data['priceRange']['buy']['booking']['max'] = my_data['max_booking_price']
    firebase_data['priceRange']['buy']['resale']['min'] = my_data['min_resale_price']
    firebase_data['priceRange']['buy']['resale']['max'] = my_data['max_resale_price']
    firebase_data['projectDetails']['projectName'] = my_data['projectName']
    firebase_data['projectDetails']['builderName'] = my_data['builderName']
    firebase_data['projectDetails']['address']['address_line1'] = my_data['address']

    temp = firebase_data['projectDetails']['projectType'].keys()
    for t in temp:
        if t.lower() in my_data['projectType'].lower():
            firebase_data['projectDetails']['projectType'][t] = True
        else:
            firebase_data['projectDetails']['projectType'][t] = False

    size =len(my_data['units'])
 
    for i in xrange(size):
        obj = my_data['units'][i].copy()
        # pprint(obj)
        temp = unit.copy()
        temp['configurations']['propertyType'] = my_data['projectType']
        temp['configurations']['type'] = obj['bhk']
        temp['configurations']['price']['booking']['min'] = obj['min_book_price']
        temp['configurations']['price']['booking']['max'] = obj['max_book_price']
        temp['configurations']['price']['resale']['min'] = obj['min_sale_price']
        temp['configurations']['price']['resale']['max'] = obj['max_sale_price']
        temp['configurations']['superArea'] = obj['superBuiltupArea']
        temp['configurations']['carpetArea'] = obj['builtupArea']
        firebase_data['units']['id'+str(i+1)] = copy.deepcopy(temp)

    for obj in firebase_data['sportsActivities']:
        if obj.lower() in my_data['amenity']:
            firebase_data['sportsActivities'][obj]=True
        else:
            firebase_data['sportsActivities'][obj]=False

    firebase_data['areas']['max'] = my_data['max_area']
    firebase_data['areas']['min'] = my_data['min_area']

    total_towers = my_data['project_detail'].split("\n")[1].split(";")[0].split()[0]
    total_units = my_data['project_detail'].split("\n")[1].split(";")[1].split()[0]
    floors = my_data['project_detail'].split("\n")[2].split()[0]

    firebase_data['projectDetails']['totalUnits'] = total_units
    firebase_data['projectDetails']['totalTowers'] = total_towers
    firebase_data['projectDetails']['floors']['max'] = floors
    firebase_data['projectDetails']['floors']['min'] = floors
    return firebase_data