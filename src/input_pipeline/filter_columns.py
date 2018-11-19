from stateless_processer import StatelessProcesser

class FilterColumns(StatelessProcesser):

    def __init__(self, incoming_address, incoming_port, outgoing_address, outgoing_port):
        def filter_columns(row):
            return [ 
                row['current shot outcome'],
                row['date'],
                row['home team'],
                row['away team'],
                row['points'],
                row['shoot team'],
                row['shoot player']]
        
        super(FilterColumns, self).__init__(incoming_address, incoming_port, outgoing_address, outgoing_port, filter_columns)