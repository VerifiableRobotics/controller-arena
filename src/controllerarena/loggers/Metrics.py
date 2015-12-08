import math
import numpy as np

class Metrics(object):
    def __init__(self):
        fid = open('log.csv', 'r')
        lines = fid.readlines()
        self.data = map(lambda x: map(lambda y: float(y), x[:-1].split(',')), lines)
        fid.close()

    def totalTime(self):
        tn = self.data[len(self.data)-1][0]
        tnstr = str(tn)
        TT = 'The total time = ' + tnstr +'[s]'
        return TT

    # def normalizedTime(self):
    #     #speed of response
    #     p1 = len(self.data)
    #
    #     xcoord = np.zeros((p1, 1))
    #     ycoord = np.zeros((p1, 1))
    #     theta = np.zeros((p1, 1))
    #     R = np.zeros((p1, 1))
    #
    #     for i in range(p1):
    #         xcoord[i,0] = self.data[i][1]
    #         ycoord[i,0] = self.data[i][2]
    #         theta[i,0] = self.data[i][3]
    #         R[i,0] = np.sqrt(np.square(xcoord[i,0]) + np.square(ycoord[i,0]))
    #
    #     dTh = np.zeros((p1, 1))
    #     dR = np.zeros((p1, 1))
    #
    #     for i in range(p1-1):
    #         dR[i,0] = R[i+1,0] - R[i,0]
    #         dTh[i,0] = theta[i+1,0] - theta[i,0]
    #
    #     Rtot = sum(dR[0:p1][0])
    #
    #     #arclength for turing radius
    #     d = 0.5 #diameter of the robot
    #     #THIS IS BOT SPECIFIC
    #     arcL = np.zeros((p1, 1))
    #     for i in range(p1-1):
    #         arcL[i,0] = d*dTh[i,0]
    #
    #     arcLtot = sum(arcL[0:p1][0])
    #
    #     # #NORMALIZING TIME
    #     distot = Rtot+arcLtot
    #     ttot = self.data[len(self.data)-1][0]
    #     ttotstr = str(ttot)
    #     tn = ttot/distot*0.01
    #     tnstr = str(tn)
    #     NormT = 'The normalized time is ' + tnstr + ' [s]'
    #     return NormT

    def chatter(self):
        p1 = len(self.data)

        xcoord = np.zeros((p1, 1))
        ycoord = np.zeros((p1, 1))
        theta = np.zeros((p1, 1))
        v = np.zeros((p1, 1))
        R = np.zeros((p1, 1))

        for i in range(p1):
            xcoord[i,0] = self.data[i][1]
            ycoord[i,0] = self.data[i][2]
            theta[i,0] = self.data[i][3]
            v[i,0] = self.data[i][4]
            R[i,0] = np.sqrt(np.square(xcoord[i,0]) + np.square(ycoord[i,0]))

        dt = self.data[1][0] - self.data[0][0]

        dTh = np.zeros((p1, 1))
        dR = np.zeros((p1, 1))
        vc = np.zeros((p1, 1)) #calcualted translational velocity
        #wc = np.zeros((p1, 1))#calcualted angular velocity
        chat = np.zeros((p1, 1))

        for i in range(p1-1):
            dR[i,0] = R[i+1,0] - R[i,0] #
            dTh[i,0] = theta[i+1,0] - theta[i,0]
            vc[i,0] = dR[i,0]/dt
            chat[i,0] = v[i,0]- vc[i,0]

        #ch_mean = np.mean(chat)
        #ch_std = np.std(chat)
        MxChat = max(chat)
        mxstr = str(MxChat)
        ChatStr = 'The maximum chatter is ' + mxstr + ' [m/s]'
        return ChatStr

    def oscillitory(self):
        p1 = len(self.data)

        xcoord = np.zeros((p1, 1))
        ycoord = np.zeros((p1, 1))
        theta = np.zeros((p1, 1))
        x_d = np.zeros((p1, 1))
        y_d = np.zeros((p1, 1))
        Th_d = np.zeros((p1, 1))


        for i in range(p1):
            xcoord[i] = self.data[i][1]
            ycoord[i] = self.data[i][2]
            theta[i] = self.data[i][3]
            x_d = self.data[0][6]
            y_d = self.data[0][7]
            Th_d = self.data[0][8]

        xdif = np.nonzero(xcoord==x_d)
        xindex = len(xdif)

        ydif = np.nonzero(ycoord==y_d)
        yindex = len(ydif)

        ps = max(xindex, yindex)
        pp = p1 - ps

        Osc = np.zeros((pp, 1))

        for i in range(pp):
            Osc[i,0] = theta[i+ps] - Th_d

        #print max(Osc)
        OSCstr = str(max(Osc))
        MxOsc = 'The maximum oscilitory motiion is ' + OSCstr + ' [rad]'
        return MxOsc

    def OverShoot(self):
        p1 = len(self.data)

        xcoord = np.zeros((p1, 1))
        ycoord = np.zeros((p1, 1))
        x_d = np.zeros((p1, 1))
        y_d = np.zeros((p1, 1))
        M_p = np.zeros((p1, 2))

        for i in range(p1):
            xcoord[i] = self.data[i][1]
            ycoord[i] = self.data[i][2]
            x_d = self.data[0][6]
            y_d = self.data[0][7]
            M_p[i,0] =  x_d - xcoord[i]
            M_p[i,1] =  y_d - ycoord[i]

        #print min(M_p[:,0])
        xos =  -1*min(M_p[:,0])
        xostr = str(xos)
        #print min(M_p[:,1])
        yos =  -1*min(M_p[:,1])
        yostr = str(yos)
        OSstr = 'The overshoot is x = ' + xostr + ' and y = ' + yostr
        return OSstr
