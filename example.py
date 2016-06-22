####################################
### NASM 2016 VNA Power Cal      ###
### Example 1:                   ###
### Commanded vs measured power  ###
####################################


from rohdeschwarz.general         import print_header
from rohdeschwarz.instruments.vna import Vna
from rohdeschwarz.instruments.vna import SweepType
import matplotlib.pyplot as plt
import numpy             as np

# Open instrument connection
vna = Vna()
vna.open('TCPIP', '127.0.0.1')

# SCPI command log
vna.open_log("SCPI Command Log.txt")
print_header(vna.log, "Measure with a1", "0.0.1")
vna.print_info()

# Preset
vna.preset()
vna.pause()
vna.clear_status()

# Setup channel 1
ch1                 = vna.channel(1)
ch1.sweep_type      = SweepType.power
ch1.start_power_dBm = -20.0
ch1.stop_power_dBm  = 0
ch1.points          = 201
ch1.if_bw_Hz        = 1, 'kilo'
ch1.cal_group       = 'example'
ch1.manual_sweep    = True

# Setup Trc1: S21
s21_trace           = vna.trace('Trc1')
s21_trace.parameter = 'S21'

# Setup Trc2: a1(P1)
vna.create_trace(channel=1, name='Trc2', parameter="a1(P1)")
a1_trace         = vna.trace('Trc2')
a1_trace.diagram = 1

# Sweep, Retrieve data
power_dBm, s21_dB = s21_trace.measure_formatted_data()
a1_dBm            = a1_trace.y_formatted

# Plot
plt.plot(power_dBm, s21_dB, 'r-', label="Ideal")
plt.plot(a1_dBm,    s21_dB, 'b-', label="Measured")
plt.legend()
plt.show()
