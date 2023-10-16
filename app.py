import requests
import os, sys
from dotenv import load_dotenv
import json
from datetime import datetime
from config import Config
from pymongo.mongo_client import MongoClient
from pymongo.database import Database
from pymongo.results import InsertOneResult
from time import sleep

load_dotenv()
config = Config(os.environ.get("BLINK_URI"), os.environ.get("BLINK_FACILITYID"), json.loads(os.environ.get("BLINK_OBJECT")), os.environ.get("BLINK_APIKEY"), os.environ.get("BLINK_MONGOURI"), int(os.environ.get("BLINK_REFRESH_SECONDS")))

def myconverter(o):
 if isinstance(o, datetime.datetime):
    return o.__str__()

def get_gym_data(conf:Config) -> dict:
    headers = {
        "x-api-key": conf.apikey
    }
    params = {"facilityId": conf.fac_id}

    res = requests.get(f"https://{conf.uri}/moso-api/activities/whoischeckedin", headers=headers, params=params)
    if res.status_code == 200:
        data = json.loads(res.content)
        data['currentCapacity'] = data['info']['CurrentlyCheckedIn']
        data['totalCapacity'] = data['info']['ClubCapacity']
        data['theTime'] = datetime.utcnow()
        data['theMeta'] = {"source": "api"}
        data['gym'] = config._facility_object['facName']
        
        data.pop('info')

        return data
    else:
        print(res.status_code)
    return {}

def save_gym_data(data: dict, db: Database, conf: Config) -> InsertOneResult:
    status = InsertOneResult
    if data:
        status = db.insert_one(data)
    return status

def main():
    try:
        client = MongoClient(config.mongo_uri)
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print("We failed")
        print(e)
        sleep(5)    
        main()
    try:    
        curr_data = get_gym_data(config)
        
        if curr_data:
            print("Saving time data")
            db = client.blinker.blinkerers
            save_status = save_gym_data(curr_data, db, config)
            with open('/tmp/test', 'w') as f:
                f.write(datetime.now().isoformat())
                f.write("\n")
                f.write(str(config))
                f.write("\n")
                
                print(curr_data)
                f.write(str(curr_data))
                # json.dump(curr_data, f, default=myconverter)
                # f.write(json.dumps(curr_data))
            print(save_status.inserted_id)
    except Exception as e:
        print("Connect failed")
        print(e)

    client.close()    
    # print(f"Sleeping for {config.seconds}")
    # sleep(config.seconds)
    return 0

if __name__ == "__main__":
    sys.exit(main())