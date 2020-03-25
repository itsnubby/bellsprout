"""
bellsprout.py - Your virtual garden container.
Public:
    * Garden(object)
modified: 3/24/2020
  ) 0 o .
"""
import os, sys, datetime, copy, json
import numpy as np
# Maintain Python2 compatibility...FOOLISHLY.
try:
    from .squawk import ask, say
except:
    from squawk import ask, say
#finally:
#    print('Error! File \'squawk\' not found! Aborting...')
#    sys.exit(1)

## Local functions.
def _save_file(contents, save_path, option='+'):
    """
    Try to save a file.
    :in: contents (str)
    :in: save_path (str)
    :in: option (str) - {+ [append], ? [query_to_overwrite], ! [overwrite]}
    """
    action = 'w'
    if os.path.isfile(save_path):
        if option == '?':
            if option == '+' or not ask('File '+save_path+' exists. Replace?', answer_type=bool):
                action += '+'
    with open(save_path, action) as fp_save:
        fp_save.write(contents)


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
        self.temperature = 0
        # If adding to location, toggle self.occupied to 'True'.
        self.occupied = False
    
    def __str__(self):
        things = [
                str(self.position[0]),
                str(self.position[1]),
                str(self.position[2]),
                str(self.light),
                str(self.water),
                str(self.humidity),
                str(self.temperature)]
        return ', '.join(things)


class Garden(object):
    """
    PUBLIC:
    This contains a 3-D map of objects that you might find in a garden,
        plus any analysis-focused methods for their placements/interractions.
    CONFIGS (see 'config' below):
    Configurations must be of the format:
    {size: [x,y,z] (float), units: {m,inches,ft,etc} (str), resolution: (float),
        party: [Plant, Structure, Condition, Other]}
    [TODO: (@nubby) add the ability to pre-load objects?]
    [TODO: (@nubby) improve to allow for slanted terrain.]
    """
    def __init__(
            self,
            name=''):
        """
        :in: name (str)
        :in: config {dict} - defined above
        """
        self.config_dir = './configs/'  # TODO: (@nubby) consider removing.
        self.lib_dir = './lib/'
        self.label = name if name else 'UNDEF_GARDEN'
        self.spacetime = []
        self.config = self.load_garden(name)
        # TODO: (@nubby) should the point-cloud be created in the init?
        self.setup(self.config)

    def __str__(self):
        return self.label

    def load_garden(self, config_label='_default'):
        """
        Try to load configurations for a garden.
        :in: config_label (str) - file name in the './configs/' directory, minus the '.json'
        :out: config {dict} - formatted as shown above
        """
        # TODO: (@nubby) import garden data too?
        config_path = ''.join([
            self.config_dir,
            config_label,
            '.json'])
        try:
            say('Loading config file from '+config_path)
            assert(os.path.isfile(config_path))
        except AssertionError:
            say('Config file '+str(config_path)+' not found; loading defaults', 'warning')
            config_path = ''.join([
                self.config_dir,
                '_default.json'])
        with open(config_path,'r') as fp_config:
            config = json.load(fp_config)
        return config

    def setup(self, config):
        """
        Creates a point-cloud of all positions in garden.
        :in: config {dict} - definied above
        """
        say('Initializing garden, '+self.label)
        try:
            # Find boundaries of garden.
            x_dim = int(config['size'][0] / config['resolution'] + 1)
            y_dim = int(config['size'][1] / config['resolution'] + 1)
            z_dim = int(config['size'][2] / config['resolution'] + 1)
            # Initialize an empty array of the right size.
            self.spacetime = [[[None for z_i in range(z_dim)] for y_i in range(y_dim)] for x_i in range(x_dim)]
            # ...and fill it on up.
            for x_i in range(x_dim):
                x = float(x_i) * config['resolution']
                for y_i in range(y_dim):
                    y = float(y_i) * config['resolution']
                    for z_i in range(z_dim):
                        z = float(z_i) * config['resolution']
                        self.spacetime[x_i][y_i][z_i] = Point([x,y,z])
            say('Garden assembled', 'success')
        except:
            say('Error assembling garden', 'error')

    def _get_garden_data(self):
        """
        Take a snapshot of this garden's point-cloud's data.
        :out: garden_data (str) - stringified CSV-formatted spacetime readout
        """
        garden_data = 'x, y, z, light, water, humidity, temperature\n'
        for xyz in self.spacetime:
            for xy in xyz:
                for coordinate in xy:
                    garden_data += str(coordinate)+'\n'
        return garden_data

    def _get_garden_config(self):
        return str(self.config).replace('\'', '"')

    def check_on_garden(self):
        """
        Take a snapshot of your garden.
        :out: garden_data (str) - CSV-formatted point-cloud data
        :out: garden_config (str) - stringified dictionary
        """
        garden_data = self._get_garden_data()
        garden_config = self._get_garden_config()
        return garden_data, garden_config

    def save_garden(self, name='_default'):
        """
        Save garden configurations to the folder, 'self.config_dir'.
        :in: name (str) - [optional] name of config file to save
        """
        if name == '_default':
            name = self.label
        # Generate file paths.
        garden_data_path = ''.join([
            self.lib_dir,
            name,
            '.csv'])
        garden_config_path = ''.join([
            self.config_dir,
            name,
            '.json'])

        # Wrangle some data.
        garden_data, garden_config = self.check_on_garden()

        _save_file(garden_data, garden_data_path)
        _save_file(garden_config, garden_config_path, option='!')


if __name__ == '__main__':
    bellsprout = Garden('bellsprout')
    bellsprout.save_garden()
