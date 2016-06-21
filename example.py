from rohdeschwarz.instruments.vna import Vna
from rohdeschwarz.general import *

# Open instrument connection
# Start SCPI command log
vna = Vna()
vna.open('TCPIP', '127.0.0.1')
vna.open_log("SCPI Command Log.txt")
print_header(vna.log, "Measure with a1", "0.0.1")
vna.print_info()

# Assume:
#   Ch1 is power sweep
#   'Trc1' is S21 trace (desired)
#   Port 1 power cal (s1, a1)

# Setup
ch1 = vna.channel(1)
s21_trace = vna.trace('Trc1')
vna.create_trace(channel=1, name='Trc2', parameter="a1(P1)")
a1_trace  = vna.trace('Trc2')

# Perform sweep
timeout_ms = 2 * channel.total_sweep_time_ms + 5000
channel.start_sweep()
vna.pause(timeout_ms)

# Retrieve data
s21_data = s21_trace.