class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    ver = '0.0'

    def do_POST(self):
        '''
        Order gets written to the DemandDB

        Use order.json to create a Dispatch
        dispatch = Dispatch(necessary json object data unpacked)

        dispatch is written to SupplyDB

        Get all vehicle whose ETA to order.address1 is within acceptable discrepancy and contain serviceType
        Dispatch gets added to chosen vehicle's dispatch queue

        '''

    def do_GET(self):
        '''
        Fleet manager probably wants some sort of access to dispatches. Might not exist here but instead in
        specifically SupplyBE handler(s)

        '''


    def do_UPDATE(self):
        '''

        '''