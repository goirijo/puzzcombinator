import puzzcombinator as pz
import numpy as np

teststring="HellotheremynameisRoberto.Ihavebiglongclawsandhungryeyes.\
Paynoattentiontothatloser.Hebelievestheundergroundisahidingspot\
forhardearnedmoney."

teststring="Hello Blanchedporcupine! Here is an example of some text you can encode with this method.\
        I would be happy to create another grid and decoder for you, if you're not experienced with python.\
        Otherwise I can give you access to my github repository."

testcoder=pz.Encoder(teststring,"test")
testcoder.draw("testdraw")
