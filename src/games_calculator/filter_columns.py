from stateless_processer import StatelessProcesser
END_TOKEN = 'END'
class FilterColumns(StatelessProcesser):

    def __init__(self, incoming_address, incoming_port, outgoing_address, outgoing_port):
        def filter_columns(x):
            return [ 
                    x[0], #Outcome
                    x[1], #Date
                    x[2], #)Home team
                    x[3], #Away team 
                    x[4], #Points
                    x[5]] #Shoot team
        
        super(FilterColumns, self).__init__(incoming_address, incoming_port, outgoing_address, outgoing_port, filter_columns)
