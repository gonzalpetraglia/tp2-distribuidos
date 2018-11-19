from stateless_processer import StatelessProcesser

class FilterScored(StatelessProcesser):

    def __init__(self, incoming_address, incoming_port, outgoing_address, outgoing_port):
        def filter_columns(x):
            return x[1:] if x[0] == 'SCORED' else None
        
        super(FilterScored, self).__init__(incoming_address, incoming_port, outgoing_address, outgoing_port, filter_columns)
