import sys

sys.path.insert(1, '../')
from utils.vehicleutils import getRoute, getEta


def main():
    test = getEta()
    print(test[1])


if __name__ == '__main__':
    main()
