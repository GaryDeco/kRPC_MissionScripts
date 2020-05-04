import krpc
import numpy as np

conn = krpc.connect()
KSC = conn.space_center
vessel = KSC.active_vessel

class DvMap(object):
    '''Object containing delta v data traveling from kerbin to any of the stock celestial bodies\n
       Note: Dv values assume ideal conditions, these are the absolute minimums!\n

       Structure:\n
       - DVMap contains a dictionary of the stock planets/moons\n
        - The keys are lower case ie.. 'duna', 'ike'
        - The values contain numpy arrays of dv data taken from the dv map cheat sheet on KSP wiki
        - link: https://wiki.kerbalspaceprogram.com/wiki/Cheat_sheet
        - array data is in the general order of [intercept_dv, low_orbit_dv, stable_orbit_dv] 
        - for parent planets (have moons) arrays are [intercept_dv, dv_to_SOI, low_orbit, stable_orbit]
        - These are meant to be a guide for mission planning, there are more accurate ways to calculate dv. 
    '''
    def __init__(self):
        # Kerbin (planet)
        self.kerbin = np.array((0,3400,1115,950))
        # Kerbin moons
        self.targets = {
            'mun': np.array((860, 310, 580)),
            'minmus': np.array((930, 160, 180)),
            # Kerbol (sun)
            'kerbol': np.array((6000, 13700, 67000)),
            # Eeloo (planet)
            'eeloo': np.array((1140, 1370, 620)),
            # Moho (planet)
            'moho': np.array((760, 2410, 870)),
            # Jool (planet)
            'jool': np.array((980, 160, 2810, 1400)),
            # Jool's moons
            'pol': np.array((160, 820, 130)),
            'bop': np.array((220, 900, 230)),
            'tylo': np.array((400, 1100, 2270)),
            'vall': np.array((620, 910, 860)),
            'laythe': np.array((930, 1070, 2900)),
            # Eve (planet)
            'eve': np.array((90,80,1330,8000)),
            # Eve moon
            'gilly': np.array((60, 410, 30)),
            # Duna (planet)
            'duna': np.array((130, 250, 360, 1450)),
            # Duna's moons
            'ike': np.array((30, 180, 390)),
            'dres': np.array((610,1290,430))
        }

    def dv_to(self,body):
        """class method to get dv from kerbin to a body or moon\n
           :param: (body) is a string in lowercase ie.. 'duna'\n
           :example: dv = DvMap().dv_to('duna') then, print(dv)       
        """       
        if body == 'kerbin':
            body = self.kerbin
            dv = sum(self.kerbin) - self.kerbin[3]

        elif body == 'mun' or body == 'minmus':
            target = self.targets[body]
            kerbin = self.kerbin[1]
            dv = kerbin + sum(target) 

        elif body =='bop' or body =='pol' or body =='tylo' or body =='vall' or body =='laythe':
            target = self.targets[body]
            parent = self.targets['jool']
            jool = sum(parent) - parent[3] - parent[2]
            kerbin = sum(self.kerbin) - self.kerbin[2]           
            dv = kerbin + jool + sum(target) 

        elif body =='gilly':
            target = self.targets[body]
            parent = self.targets['eve']
            eve = sum(parent) - parent[3] - parent[2]
            kerbin = sum(self.kerbin) - self.kerbin[2]           
            dv = kerbin + eve + sum(target)

        elif body =='ike':
            target = self.targets[body]
            parent = self.targets['duna']
            duna = sum(parent) - parent[3] - parent[2]
            kerbin = sum(self.kerbin) - self.kerbin[2]           
            dv = kerbin + duna + sum(target)

        else:
            target = self.targets[body]
            kerbin = sum(self.kerbin) - self.kerbin[2]
            dv = kerbin + sum(target)
     
        return dv

        

            





        
