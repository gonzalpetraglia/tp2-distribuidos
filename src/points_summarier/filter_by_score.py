from stateless_processer import StatelessProcesser

class FilterByScore(StatelessProcesser):

    def __init__(self, points_filter, incoming_address, incoming_port, outgoing_address, outgoing_port):
        def filter_columns(x):
            return x if str(x[1]) == str(points_filter) else None
        
        super(FilterByScore, self).__init__(incoming_address, incoming_port, outgoing_address, outgoing_port, filter_columns)
