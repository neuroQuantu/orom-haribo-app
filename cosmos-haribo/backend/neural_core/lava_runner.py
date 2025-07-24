import numpy as np
from lava.proc.lif.process import LIF
from lava.proc.dense.process import Dense
from lava.magma.core.run_conditions import RunSteps

def run_snn_inference(data):
    lif = LIF(shape=(100,), du=100, dv=10)
    dense = Dense(weights=np.random.rand(100, 50))
    lif.out_ports.s_out.connect(dense.in_ports.s_in)
    lif.run(condition=RunSteps(num_steps=100))
    lif.stop()
    return {"status": "inference complete"}
