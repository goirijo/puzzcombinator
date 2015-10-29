import encoder
import numpy as np

teststring="HellotheremynameisRoberto.Ihavebiglongclawsandhungryeyes.\
            Paynoattentiontothatloser.Hebelievestheundergroundisahidingspot\
            forhardearnedmoney."


grid=encoder.R4(teststring)

traced=encoder.trace_R4(teststring,grid)
canvas=traced.copy()
for rot in range(4):
    canvas[:,:]=" "
    canvas[grid]=traced[grid]
    print canvas.T
    print ""
    grid=np.rot90(grid)

print traced.T
print grid.T.astype(int)

encoder.draw_grid("grid.svg",grid)
encoder.draw_decoder("decoder.svg",grid)
