from stateful_processer_unique import StatefulProcesserUnique

class SumUpPoints(StatefulProcesserUnique):
    def __init__(self, incoming_address, incoming_port, outgoing_address, outgoing_port):
        def init_state():
            return {"scored": 0, "total": 0}
        
        def update_state(accumulator, shot):
            accumulator["total"] += 1
            if shot[0] == "SCORED":
                accumulator["scored"] += 1


        def get_summaries(accumulator):
            scored_shots = accumulator["scored"]
            total_shots = accumulator["total"]
            yield '{}%'.format(float(scored_shots) / total_shots * 100) if total_shots else 'undefined'

        super(SumUpPoints, self).__init__(incoming_address, 
                                            incoming_port,
                                            outgoing_address,
                                            outgoing_port,
                                            init_state,
                                            update_state,
                                            get_summaries)
