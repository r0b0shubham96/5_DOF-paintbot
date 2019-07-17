import math
import _thread
import time
import RPi.GPIO as GPIO #this library is entirely for valve functioning
from time import sleep
from Stepper import stepper # For movement of arm from one point to another point, this STepper program contains code to run movement in steps

import array

tx = 0;
ty = 0;
tz = 0;

q1=[math.degrees(math.atan2(ty, tx)), math.degrees(math.atan2(-ty, -tx))]

arrC1 = array.array('d')
arrS1 = array.array('d')

for i in range(len(q1)):
    arrC1.append(math.cos(q1[i]*math.pi/180))

for i in range(len(q1)):
    arrS1.append(math.sin(q1[i]*math.pi/180))

C1 = arrC1[0]
S1 = arrS1[0]

q2=[ math.degrees(math.atan2((49*C1**2*S1*ty)/500 - C1**2*tx**2 + C1**2*ty**2 - 2*C1*S1*tx*ty + (49*C1*tx)/500 + (49*S1**3*ty)/500 - ty**2 - tz**2 - 2401/1000000, -((265923*C1**6*ty**2)/250000 + (49*C1**4*S1*tx**2*ty)/250 - (49*C1**4*S1*ty**3)/250 - C1**4*tx**4 + 6*C1**4*tx**2*ty**2 - C1**4*ty**4 - (797769*C1**4*ty**2)/250000 - 4*C1**3*S1*tx**3*ty + 4*C1**3*S1*tx*ty**3 + (265923*C1**3*S1*tx*ty)/125000 + (49*C1**3*tx**3)/250 - (147*C1**3*tx*ty**2)/250 + (49*C1**2*S1**3*tx**2*ty)/250 - (49*C1**2*S1**3*ty**3)/250 + (49*C1**2*S1*tx**2*ty)/125 + (49*C1**2*S1*ty**3)/250 + (49*C1**2*S1*ty*tz**2)/250 - (26178103*C1**2*S1*ty)/250000000 - 6*C1**2*tx**2*ty**2 - 2*C1**2*tx**2*tz**2 + (105889*C1**2*tx**2)/100000 + 2*C1**2*ty**4 + 2*C1**2*ty**2*tz**2 + (1066093*C1**2*ty**2)/500000 + (265923*C1*S1**3*tx*ty)/125000 - 4*C1*S1*tx*ty**3 - 4*C1*S1*tx*ty*tz**2 - (2401*C1*S1*tx*ty)/250000 + (147*C1*tx*ty**2)/250 + (49*C1*tx*tz**2)/250 - (26178103*C1*tx)/250000000 + (265923*S1**6*ty**2)/250000 + (49*S1**3*ty**3)/250 + (49*S1**3*ty*tz**2)/250 - (26178103*S1**3*ty)/250000000 - ty**4 - 2*ty**2*tz**2 - (2401*ty**2)/500000 - tz**4 + (534247*tz**2)/500000 + 514243779/200000000000)**(1/2))) - math.degrees(math.atan2(- 1036000*ty*C1**2*S1 - 1036000*tx*C1 - 1036000*ty*S1**3 + 50764, -1036000*tz)), math.degrees(math.atan2((49*C1**2*S1*ty)/500 - C1**2*tx**2 + C1**2*ty**2 - 2*C1*S1*tx*ty + (49*C1*tx)/500 + (49*S1**3*ty)/500 - ty**2 - tz**2 - 2401/1000000, ((265923*C1**6*ty**2)/250000 + (49*C1**4*S1*tx**2*ty)/250 - (49*C1**4*S1*ty**3)/250 - C1**4*tx**4 + 6*C1**4*tx**2*ty**2 - C1**4*ty**4 - (797769*C1**4*ty**2)/250000 - 4*C1**3*S1*tx**3*ty + 4*C1**3*S1*tx*ty**3 + (265923*C1**3*S1*tx*ty)/125000 + (49*C1**3*tx**3)/250 - (147*C1**3*tx*ty**2)/250 + (49*C1**2*S1**3*tx**2*ty)/250 - (49*C1**2*S1**3*ty**3)/250 + (49*C1**2*S1*tx**2*ty)/125 + (49*C1**2*S1*ty**3)/250 + (49*C1**2*S1*ty*tz**2)/250 - (26178103*C1**2*S1*ty)/250000000 - 6*C1**2*tx**2*ty**2 - 2*C1**2*tx**2*tz**2 + (105889*C1**2*tx**2)/100000 + 2*C1**2*ty**4 + 2*C1**2*ty**2*tz**2 + (1066093*C1**2*ty**2)/500000 + (265923*C1*S1**3*tx*ty)/125000 - 4*C1*S1*tx*ty**3 - 4*C1*S1*tx*ty*tz**2 - (2401*C1*S1*tx*ty)/250000 + (147*C1*tx*ty**2)/250 + (49*C1*tx*tz**2)/250 - (26178103*C1*tx)/250000000 + (265923*S1**6*ty**2)/250000 + (49*S1**3*ty**3)/250 + (49*S1**3*ty*tz**2)/250 - (26178103*S1**3*ty)/250000000 - ty**4 - 2*ty**2*tz**2 - (2401*ty**2)/500000 - tz**4 + (534247*tz**2)/500000 + 514243779/200000000000)**(1/2))) - math.degrees(math.atan2(- 1036000*ty*C1**2*S1 - 1036000*tx*C1 - 1036000*ty*S1**3 + 50764, -1036000*tz))]

arrC2 = array.array('d')
arrS2 = array.array('d')

for i in range(len(q2)):
    arrC2.append(math.cos(q2[i]*math.pi/180))

for i in range(len(q2)):
    arrS2.append(math.sin(q2[i]*math.pi/180))

C2 = arrC2[0]
S2 = arrS2[0]

q3=[math.degrees(math.atan2(259/500, -((12691*C2)/250000 - (49*C1*tx)/500 - (49*S1*ty)/500 - (259*S2*tz)/250 + ty**2 + tz**2 + C1**2*tx**2 - C1**2*ty**2 - (259*C1*C2*tx)/250 - (259*C2*S1*ty)/250 + 2*C1*S1*tx*ty + 2401/1000000)**(1/2))) - math.degrees(math.atan2(1000*S2*tz - 49*C2 + 1000*C1*C2*tx + 1000*C2*S1*ty - 518, 49*S2 + 1000*C2*tz - 1000*C1*S2*tx - 1000*S1*S2*ty)), math.degrees(math.atan2(259/500, ((12691*C2)/250000 - (49*C1*tx)/500 - (49*S1*ty)/500 - (259*S2*tz)/250 + ty**2 + tz**2 + C1**2*tx**2 - C1**2*ty**2 - (259*C1*C2*tx)/250 - (259*C2*S1*ty)/250 + 2*C1*S1*tx*ty + 2401/1000000)**(1/2))) - math.degrees(math.atan2(1000*S2*tz - 49*C2 + 1000*C1*C2*tx + 1000*C2*S1*ty - 518, 49*S2 + 1000*C2*tz - 1000*C1*S2*tx - 1000*S1*S2*ty))]

arrC3 = array.array('d')
arrS3 = array.array('d')

for i in range(len(q3)):
    arrC3.append(math.cos(q3[i]*math.pi/180))

for i in range(len(q3)):
    arrS3.append(math.sin(q3[i]*math.pi/180))

C3 = arrC3[0]
S3 = arrS3[0]

q4 = [0, 0]

arrC4 = array.array('d')
arrS4 = array.array('d')

for i in range(len(q4)):
    arrC4.append(math.cos(q4[i]*math.pi/180))

for i in range(len(q4)):
    arrS4.append(math.sin(q4[i]*math.pi/180))

C4 = arrC4[0]
S4 = arrS4[0]

q5=math.degrees(atan2(C1*ny - S1*nx, C2*C3*S4*nx + C2*C4*S3*nx + C3*C4*S2*nx - S2*S3*S4*nx - C2*S1*S3*S4*ny - C3*S1*S2*S4*ny - C4*S1*S2*S3*ny + C1*C2*C3*C4*nx + C2*C3*C4*S1*ny - C1*C2*S3*S4*nx - C1*C3*S2*S4*nx - C1*C4*S2*S3*nx)), math.degrees(math.atan2(S1*nx - C1*ny, S2*S3*S4*nx - C2*C4*S3*nx - C3*C4*S2*nx - C2*C3*S4*nx + C2*S1*S3*S4*ny + C3*S1*S2*S4*ny + C4*S1*S2*S3*ny - C1*C2*C3*C4*nx - C2*C3*C4*S1*ny + C1*C2*S3*S4*nx + C1*C3*S2*S4*nx + C1*C4*S2*S3*nx))


