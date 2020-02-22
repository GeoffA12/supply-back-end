import random
vehicles = [
    {
        "vid" : 12345,
        "serviceType" : "DryCleaning",
        "vehicleMake" : "Toyota",
        "liscencePlate" : "QW3456",
        "status" : "Delivering",
        "location" : {
            "lon" : 23.42,
            "lat" : 42.12,
        },
        "destination" : {
            "address1" : "3001 S Congress Ave",
            "address2" : "St. Andres RM222D"
        }
    },
    {
        "vid" : 98765,
        "serviceType" : "PartyPlanner",
        "vehicleMake" : "Tesla",
        "liscencePlate" : "TE1241",
        "status" : "Delivered",
        "location" : {
            "lon" : 45.12,
            "lat" : 10.31,
        },
        "destination" : {
            "address1" : "",
            "address2" : ""
        }
    }
]

class returnCar():
    def do_POST(self):
        return vehicles[random.randint(0,1)]
def main():
    hold = returnCar()
    vehicle = hold.do_POST()
    print(vehicle)

if __name__ == '__main__':
    main()