import rill


class EndExecution(Exception):
    pass


@rill.component
@rill.inport('SINK')
def finish(SINK):
    SINK.close()
    # HACK: Really terrible hack
    print(EndExecution('End of Program'))
    import sys
    sys.exit(0)
