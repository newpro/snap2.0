import pyrebase
import json
from errs import ParaErr, MountErr, DataErr, KeyErr, LoadedErr

# --- set up ---
with open('secret.json') as data_file:    
    secrets = json.load(data_file)
config = secrets['config']
runtime = secrets['runtime']
firebase = pyrebase.initialize_app(config)
db = firebase.database()
mod = runtime['mod']
# token for write
token = firebase.auth().sign_in_with_email_and_password(secrets['user']['email'],
                                        secrets['user']['password'])['idToken']

def _mount(mount_point, loc = '', request_ref = False):
    """
    Helper Function
    check validility of a mount point (only during testing), and then mount the data point, return the reference
    Optional, loc: specify a attached data location, this location will not be checked for validility
    Optional, ref: return a reference point instead of a path string
    
    Return: 
    if ref is false, will return a string indicate the path of the data
    otherwise it will return the reference of the data
    -
    Warning:
    If reference get returned, this statement has to append with a get to clear path data!
    Otherwise it will interfere with other mount
    Read this git issue: 
    https://github.com/thisbejim/Pyrebase/issues/56
    -
    For a wrong usage example:
    print _mount('hardwares/objects')
    print _mount('knowledge/sensor_types').get().val()
    
    Error:
    Mount point or data in mount point not exists,
    this will only be checked in testing, for deploy environment
    
    # Check if mount_point exists
    >>> _mount('hardwares/sensors', path_only=True)
    hardwares/sensors/
    
    # Check if data exists at mount_point
    >>> _mount('hardwares/sensors', 'kinect1', path_only=True)
    hardwares/sensors/kinect1
    
    # Mount a data point
    _mount('mount_point').get().val()
    """
    if mount_point[-1] == '/':
        path = mount_point + loc
    else:
        path = mount_point + '/' + loc
    if (mod == "TESTING" and not (db.child(mount_point).get().val())):
        raise MountErr('Mount point invalid: ' + mount_point)
    if request_ref:
        return db.child(path)
    return path

def _data(mount_point):
    """
    Helper Function
    request data segment of a mount point
    
    Return:
    Directory, Data from the mount point
    
    # get data from a mount point
    _data('knowledge/sensor_types')
    """
    return _mount(mount_point, request_ref=True).get().val()

def _write(path, key, value, overwrite = False):
    """
    Helper Function
    Insert a key value pair to assigned path location
    Optional: overwrite the data
    
    Notes:
    This function is differet from _write function.
    It enforces key value pairs and have in theory O(1) access/write time
    
    Error:
    Duplicate key pair exists
    
    Return:
    None for success insert
    
    >>> _set('knowledge/sensor_types', 'new_type', {'info1': '1', 'info2': 2})
    None
    """
    if (not key) or (not value):
        raise DataErr('Write data can not be empty')
    if not overwrite: # if not allow duplicate key
        if key in _data(path).keys():
            raise KeyErr('Duplicate key not allowed:' + key)
    
    _mount(path, loc = key, request_ref=True).set(value, token)

def _append(path, data):
    """
    Helper Function
    Write data to a path location
    
    Notes:
    This function is different from _insert function
    It only appends data to the path location.
    """
    return _mount(path, request_ref=True).push(data, token)

def _to_dict(data, type_allowed=['dict', 'list', 'str']):
    """
    Helper Function
    Check if this data is a list or Dict
    If it is a Dict, do nothing
    If it is a list, convert to dict, which key is the value, and value is True
    This is due to firebase best practice for speed up check time
    
    >>> _to_dict({'a': 'b'})
    {'a': 'b'}
    
    >>> _to_dict(['a', 'b'])
    {'a': True, 'b': True}
    """
    d = {}
    if (('list' in type_allowed) and isinstance(data, list)):
        for i in data:
            d[i] = True
    elif (('dict' in type_allowed) and isinstance(data, dict)):
        d = data
    elif (('str' in type_allowed) and isinstance(data, str)):
        d = data
    else:
        raise ParaErr('Unsupport Data Type: ' + data)
    return d

def _unpack(options, required = [], optional = []):
    """
    Helper Function
    Unpack the data from on options parameter according to required and optional parameter.
    At the same time, if the field is a list, convert to key value pair format, firebase parctice
    If a required parameter is missing, raise an error
    If An optional parameter is missing, ignore
    Optional: required, a list of parameters that is required
    Optional: optional, a list of parameters that is optional

    Return:
    Dictionary, the data that is repacked
    
    >>> _pack({'r1': 'a', 'r2': 'b', 'o1': 'c', 'o2': 'd'}, required=['r1', 'r2'], optional=['o1', 'o2', 'o3'])
    {'o2': 'd', 'r1': 'a', 'r2': 'b', 'o1': 'c'}
    
    # Automatically repack list to dict
    >>> _pack({'a': ['1', '2'], 'b': 'c'}, required = ['a'], optional=['b'])
    {'a': {'1': True, '2': True}, 'b': 'c'}
    """
    data = {}
    for para in required:
        if (not (para in options)):
            raise ParaErr('Required parameter missing: ' + para)
        data[para] = _to_dict(options[para])
    for para in optional:
        if (para in options):
            data[para] = _to_dict(options[para])
    return data

# ---- Generic Database Object ----
class _DBObject():
    """
    Generic database object
    This is used for inheretence of all objects that referenced to a database object
    For Internal usage only
    """
    def __init__(self, path, settings):
        self.name = None
        try:
            if settings:
                self._path = _mount(settings.path)
            else:
                self._path = _mount(path)
        except:
            raise MountErr('Unable to mount path')
    
    def new(self, name, data):
        """
        Create a new object in DB
        """
        if (self.name):
            raise LoadedErr('Object already loaded')    
        if (name[0] == '_'):
            raise ParaErr('name start with "_" is not allowed')
        for letter in name:
            if not (letter.islower() or (letter == '_')):
                raise ParaErr('Only lower case letter or "_" allowed')
        _write(self._path, name, data)
        self._path = _mount(self._path + name)
        self.name = name
    
    def hook(self, name):
        """
        Hook up with one object that has the name
        """
        if (self.name):
            raise LoadedErr('Object already loaded')
        self._path = _mount(self._path + name)
        self.name = name
    
    def data(self):
        """
        Get data of the object
        """
        return _data(self._path)

# ---- Room Management----
class Room(_DBObject):
    """
    Room Interface
    
    Public access variable:
    name: the name of the room
    """
    def __init__(self, settings = {}):
        _DBObject.__init__(self, 'hardwares/rooms', settings)
    
    def new(self, name):
        """
        Create a new room with name
        
        # Create a new room
        Room().new('newroom')
        """
        _DBObject.new(self, name, True)
        return self
    
    def hook(self, name):
        """
        Hook up with a existing room
        
        # Hook up and access the name of the room        
        Room().hook('kitchen').name
        kitchen
        """
        _DBObject.hook(self, name)
        return self

# ---- Object ----
class Object(_DBObject):
    """
    Object interface
    """
    def __init__(self, settings = {}):
        """
        Object Interface Entry Point
        """
        _DBObject.__init__(self, 'hardwares/objects', settings)
    
    def _be_watched(self, sensor, object_state, sensor_state, overwrite=True):
        """
        Helper function
        Write 
        
        Warning:
        Only write to object will break data integrity, should not be used alone
        
        """
        if not self.name:
            raise ParaErr('Object has not loaded yet')
        # Check if the object state exist for object
        if not (object_state in self.get_states()):
            raise ParaErr('object_state is not one of the_object states')
        if not (isinstance(sensor, Sensor)):
            raise ParaErr('sensor should be a Sensor object')
        if not sensor.name:
            raise ParaErr('sensor has not be hooked')
        return _write(self._path, 'watchers/' + object_state, {'sensor': sensor.name, 'state': sensor_state}, overwrite=overwrite)
    
    def get_states(self):
        """
        get all states this object can present
        
        Return:
        Dictionory, states
        """
        return self.data()['status']['states']
        
    def hook(self, name):
        _DBObject.hook(self, name)
        return self
    
    def new(self, name, location, states, description = ''):
        """
        Create a new Object, with location and states
        location: a room object
        states: a list of string, represent all status it can has.
        - Definition of a states group: 
        - If one state in states group is true, it means all others are false.
        - For example: for a states group ['on', 'off'], if on is true, off would be false.
        Optional: description, A string for short description
        
        room = Room().hook('kitchen')
        Object().new('new', room, ['on', 'off'], description='some desc')
        """
        data = {}
        if (not isinstance(location, Room)):
            raise ParaErr('location has to be a room object')
        if (description):
            data['description'] = description
        data['status'] = {
            'location': location.name,
            'states': _to_dict(states)
        }
        _DBObject.new(self, name, data)
        return self

# ---- SENSOR MANAGER ----
class SensorType(_DBObject):
    """
    Sensor Type Object interface
    One sensor type come with:
    1. reliability: the probability of one sensor reading over the actual reading
    2. multiple: If this sensor is watching several objects
    3. states: a list indicates all possible states a sensor type can has
    """
    def __init__(self, settings={}):
        _DBObject.__init__(self, 'knowledge/sensor_types', settings)
    
    def hook(self, name):
        """
        Hook up with one of the sensor type
        
        Example: 
        # access reliability of a sensor type
        SensorType().hook('binary').data()['reliability']
        """
        _DBObject.hook(self, name)
        return self
    
    def new(self, name, reliability, states, result_type, multiple=False):
        """
        Example:
        # Create a binary sensor type
        binary_type = SensorType().new('binary', 0.9, ['on', 'off'], 'binary_result')
        """
        _DBObject.new(self, name, {
            'reliability': reliability,
            'multiple': multiple,
            'result_type': result_type,
            'states': _to_dict(states, type_allowed=['list'])
        })
        return self
    
    def get_states(self):
        """
        get all state this sensor type can present
        
        Return:
        Dictonary
        """
        if not self.name:
            return None
        return self.data()['states']

class Sensor(_DBObject):
    def __init__(self, settings = {}):
        _DBObject.__init__(self, 'hardwares/sensors', settings)
    
    def get_states(self):
        """
        Get all the states this sensor can present
        """
        s_type = self.data()['type']
        return SensorType().hook(s_type).get_states()
    
    def new(self, name, sensor_type, description = ''):
        """
        Create a new sensor
        
        Example:
        type_b = SensorType().hook('binary')
        Sensor().new('new_sensor', type_b, description = 'a new sensor')
        """
        if (not isinstance(sensor_type, SensorType)):
            raise ParaErr('sensor_type has to be an SensorType object')
        _DBObject.new(self, name, {
            'type': sensor_type.name,
            'description': description
        })
        return self
    
    def hook(self, name):
        _DBObject.hook(self, name)
        return self
    
    def watch(self, the_object, sensor_state, object_state):
        """
        Establish a map to a sensor state to a object state
        So when there is a object state change, the sensor will respond
        
        Structure relationship:
        One sensor state can map to one object state.
        One object state can map to many sensor state.
        
        Performance Requirements:
        O(1) access time on both sides:
        For an object state, locate the sensor that is watching
        Key: object state, value: sensor state
        For a sensor state, locate the object that it is watching
        Key: sensor state, value: object state
        
        Return:
        None for successful mapping
        
        Example:
        Sensor().hook('new_sensor').watch('off', Object().hook('new'), 'on')
        """
        if (not isinstance(the_object, Object)):
            raise ParaErr('the_object parameter has to be Object')
        # Check if the sensor has the sensor state
        if not (sensor_state in self.get_states()):
            raise ParaErr('sensor state is not one of this sensor state')
        
        _write(self._path, 'watch/' + sensor_state, {'object': the_object.name, 'state': object_state}, overwrite=True)
        the_object._be_watched(self, object_state, sensor_state)
    
    def overwatch(self, the_object):
        """
        Shortcut function
        Specify a object to watch
        This will automatically establish one to one mapping by names of object's and sensor's states
        
        Warning:
        This method is not based on watch method
        The reason is object and sensor states data only have to fetch once to check.
        A reminder that change in one implementation in future is required to change both.
        
        Example:
        Sensor().hook('new_sensor').overwatch(Object().hook('new'))
        """
        if (not isinstance(the_object, Object)):
            raise ParaErr('the_object should be a Object object')
        
        # one to one checking
        object_states = the_object.get_states().keys()
        sensor_states = self.get_states().keys()
        if set(object_states) != set(sensor_states):
            raise ParaErr('the object does not have one to one state mapping with the sensor')
        for state in object_states:
            _write(self._path, 'watch/' + state, {'object': the_object.name, 'state': state}, overwrite=True)
            the_object._be_watched(self, state, state)
