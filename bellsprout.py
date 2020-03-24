"""
bellsprout.py - Your virtual garden container.
Public:
    * Garden(object)
modified: 3/23/2020
  ) 0 o .
"""
import os, sys
import datetime
import numpy as np
import copy

## Local functions.
def _get_time_now(time_format='utc'):
  """
  Thanks Jon.  (;
  :in: time_format (str) ['utc','epoch']
  :out: timestamp (str)
  """
  if time_format == 'utc' or time_format == 'label':
    return datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
  elif time_format == 'epoch' or time_format == 'timestamp':
    td = datetime.datetime.utcnow() - datetime.datetime(1970,1,1)
    return str(td.total_seconds()).replace('.','_')
  else:
    # NOTE: Failure to specify an appropriate time_format will cost
    #         you one layer of recursion! YOU HAVE BEEN WARNED.  ) 0 o .
    return _get_time_now(time_format='epoch')

def _check_template_path(template_path):
    """
    Test the test template at a given path.
    :out: (Bool) valid path?
    """
    if not os.path.isfile(template_path):
        return False
    elif template_path.split('.')[-1]!='json':
        return False
    return True

def _say(prompt, flag='status'):
    """
    Local print function.
    :in: prompt (str)
    :in: flag (str) - {status, success, error, warning, misc}
    """
    now = _get_time_now('timestamp')
    outfields = [now, ': ', prompt]
    if flag == 'status':
        outfields.append('...')
    elif flag == 'success':
        outfields.append('!')
    else:
        outfields.append('.')
    output = ''.join(outfields)
    print(output)

class Point(object):
    """
    PRIVATE:
    This describes a position within a Garden object in 3D space and includes
        info including:
        * coordinates [x,y,z]
        * light rating (*TODO @nubby*)
        * water rating (*TODO @nubby*)
        * humidity rating (*TODO @nubby*)
    """
    def __init__(
            self,
            position):
        """
        :in: position [x,y,z] (float)
        """
        self.position = position
        self.light = 0
        self.water = 0
        self.humidity = 0
        # If adding to location, toggle self.occupied to 'True'.
        self.occupied = False
    
    def __str__(self):
        things = [
                '[',str(self.position[0]),
                ',',str(self.position[1]),
                ',',str(self.position[2]),']']
        return ''.join(things)


class Garden(object):
    """
    PUBLIC:
    This contains a 3-D map of objects that you might find in a garden,
        plus any analysis-focused methods for their placements/interractions.
    CONFIGS (see 'configs' below):
    Configurations must be of the format:
    {size: [x,y,z] (float), units: {m,inches,ft,etc} (str), resolution: (float)}
    [TODO: (@nubby) add the ability to pre-load objects?]
    [TODO: (@nubby) improve to allow for slanted terrain.]
    """
    def __init__(
            self,
            name='',
            configs={}):
        """
        :in: name (str)
        :in: configs {dict} - defined above
        """
        self.label = name
        self.points = []
        # TODO: (@nubby) should the point-cloud be created in the init?
        self.setup(configs)

    def setup(
            self,
            configs):
        """
        Creates a point-cloud of all positions in garden.
        :in: configs {dict} - definied above
        """
        _say('Initializing garden, '+self.label)
#        try:
        # Find boundaries of garden.
        x_dim = int(configs['size'][0] / configs['resolution'] + 1)
        y_dim = int(configs['size'][1] / configs['resolution'] + 1)
        z_dim = int(configs['size'][2] / configs['resolution'] + 1)
        self.points = [[[None for z_i in range(z_dim)] for y_i in range(y_dim)] for x_i in range(x_dim)]
        for x_i in range(x_dim):
            x = float(x_i) * configs['resolution']
            for y_i in range(y_dim):
                y = float(y_i) * configs['resolution']
                for z_i in range(z_dim):
                    z = float(z_i) * configs['resolution']
                    self.points[x_i][y_i][z_i] = Point([x,y,z])
                    _say('Generated point '+str(self.points[x_i][y_i][z_i]), 'success')
        _say('Garden assembled', 'success')
        sys.exit(1)
#            _say('Creating new point at ['+str(x)+', '+str(y)+', '+str(z)+']', 'success')
#            newPoint = Point([x,y,z])
#            self.points.append(copy.deepcopy(newPoint))
#        except:
#            _say('Error assembling garden', 'error')

if __name__ == '__main__':
    def_configs = {
            'size': [10.0,10.0,42.0],
            'units': 'm',
            'resolution': 0.1
            }
    bellsprout = Garden('bellsprout', def_configs)
