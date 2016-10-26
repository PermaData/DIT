import gevent
import signal
from ..rill import rill


@rill.component
@rill.inport('SINK')
def finish(SINK):
    SINK.receive().drop()
    gevent.shutdown()
