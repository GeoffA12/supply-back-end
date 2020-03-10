import sys

sys.path.insert(1, '../')
from SERVER_UTILS.vehicle_utils import getRoute, getEta

def main():
    test = getEta()
    print(test[1])

if __name__ == '__main__':
    main()