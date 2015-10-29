import puzzcombinator as pz
import numpy as np

teststring="HellotheremynameisRoberto.Ihavebiglongclawsandhungryeyes.\
Paynoattentiontothatloser.Hebelievestheundergroundisahidingspot\
forhardearnedmoney."


grid=pz.encoder.R4.make(teststring)

traced=pz.encoder.R4.trace(teststring,grid)
canvas=traced.copy()
for rot in range(4):
    canvas[:,:]=" "
    canvas[grid]=traced[grid]
    print canvas.T
    print ""
    grid=np.rot90(grid)

print traced.T
print grid.T.astype(int)

pz.encoder.draw_grid("grid.svg",grid)
pz.encoder.draw_decoder("decoder.svg",grid)
pz.encoder.draw_encoded("encoded.svg",traced,teststring)
