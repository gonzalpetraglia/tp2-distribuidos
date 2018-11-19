from stateless_processer import StatelessProcesser

class FilterColumns(StatelessProcesser):

    def __init__(self, incoming_address, incoming_port, outgoing_address, outgoing_port):
        def filter_columns(row):
            return [ 
                    row[0], #Outcome
                    row[4], #Points
                    row[6]] #Shoot player
        
        super(FilterColumns, self).__init__(incoming_address, incoming_port, outgoing_address, outgoing_port, filter_columns)
