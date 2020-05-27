import json
from types import MappingProxyType
from datagen.constants import VALID_DATA_TYPES
from datagen.constants import VALID_NAMED_TYPES
from datagen.constants import VALID_FIELD_NAMED_TYPES
from datagen.constants import VALID_OUTPUT_FORMATS
from datagen.constants import VALID_SOURCES

def _validate_mandatory_types(field, value, data_type):
    if not value:
        raise SchemaParseException("Schema must have a non-empty {0}.".format(field))
    elif not isinstance(value, data_type):
        raise SchemaParseException("The {0} property must be {1}.".format(field, str(data_type)))

def _validate_optional_types(field, value, data_type):
    if value and not isinstance(value, data_type):
        raise SchemaParseException("The {0} property must be {1}.".format(field, str(data_type)))

def _validate_names_or_values(given_values, permitted_values):
    invalid_named_types = set(given_values) - set(permitted_values)
    if len(invalid_named_types) > 0:
        raise SchemaParseException("Invalid values/types {0} found. Valid values are {1}".format(invalid_named_types, permitted_values))

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class SchemaParseException(Error):
    pass

class Field(object):
    """Renders details of a field."""
    def __init__(self, name, type, index, min_length=None, 
        max_length=None, min_value=None, max_value=None, format=None, values=None):
        # Ensure valid mandatory arguments name and type
        _validate_mandatory_types("name", name, str)
        _validate_mandatory_types("type", type, str)
        # validate data type of the field against valid values
        _validate_names_or_values([type], VALID_DATA_TYPES)
        # Ensure optional arguments have valid types
        _validate_optional_types("min_length", min_length, int)
        _validate_optional_types("max_length", max_length, int)
        _validate_optional_types("min_value", min_value, (int,str))
        _validate_optional_types("max_value", max_value, (int,str))
        _validate_optional_types("format", format, str)
        _validate_optional_types("values", values, list)

        # add members
        self._props = {}
        self._props['name'] = self._name = name
        self._props['type'] = self._type = type
        self._props['min_length'] = self._min_length = min_length
        self._props['max_length'] = self._max_length = max_length
        self._props['min_value'] = self._min_value = min_value
        self._props['max_value'] = self._max_value = max_value
        self._props['format'] = self._format = format
        self._props['values'] = self._values = values

    # read-only properties
    @property
    def name(self):
        return self._name
    
    @property
    def type(self):
        return self._type
    
    @property
    def min_length(self):
        return self._min_length
    
    @property
    def max_length(self):
        return self._max_length
    
    @property
    def min_value(self):
        return self._min_value
    
    @property
    def max_value(self):
        return self._max_value
    
    @property
    def format(self):
        return self._format
    
    @property
    def values(self):
        return self._values
    
    @property
    def props(self):
        return self._props

class Names(object):
    """Renders details about named fields."""
    
    def __init__(self, name, output_format, output_rec_cnt, source, seed, output_file):
        # Ensure valid arguments
        _validate_mandatory_types("name", name, str)
        _validate_mandatory_types("output_format", output_format, str)
        # validate output format against permitted values
        _validate_names_or_values([output_format], VALID_OUTPUT_FORMATS)
        _validate_mandatory_types("output_rec_cnt", output_rec_cnt, int)
        _validate_mandatory_types("source", source, str)
        # validate source against permitted values
        _validate_names_or_values([source], VALID_SOURCES)
        _validate_mandatory_types("seed", seed, int)
        _validate_mandatory_types("output_file", output_file, str)

        # add properties
        self._props = {}
        self._props['name'] = self._name = name
        self._props['output_format'] = self._output_format = output_format
        self._props['output_rec_cnt'] = self._output_rec_cnt = output_rec_cnt
        self._props['source'] = self._source = source
        self._props['seed'] = self._seed = seed
        self._props['output_file'] = self._output_file = output_file

    # read-only properties
    @property
    def name(self):
        return self._name
    
    @property
    def output_format(self):
        return self._output_format
    
    @property
    def output_rec_cnt(self):
        return self._output_rec_cnt
    
    @property
    def source(self):
        return self._source
    
    @property
    def seed(self):
        return self._seed
    
    @property
    def output_file(self):
        return self._output_file

    @property
    def props(self):
        return self._props

class Schema(object):
    """JSON Schema Object."""
    @staticmethod
    def _make_field(index, field_data):
        """Builds field schemas from a list of field JSON descriptors.
        Args:
            index: 0-based index of the field in the record.
            field_data: JSON descriptors of a record field.
        Return:
            The field schema.
        """
        #check if only valid field object types are provided
        _validate_names_or_values(field_data.keys(), VALID_FIELD_NAMED_TYPES)
        return Field(
            name = field_data.get('name'),
            type = field_data.get('type'),
            index=index,
            min_length = field_data.get('min_length', None),
            max_length = field_data.get('max_length', None),
            min_value = field_data.get('min_value', None),
            max_value = field_data.get('max_value', None),
            format = field_data.get('format', None),
            values = field_data.get('values', None)
        )

    @staticmethod
    def _make_field_list(fields_data):
        """Builds field schemas from a list of field JSON descriptors.
        Guarantees field name unicity.
        Args:
            fields_data: collection of field JSON descriptors.
        Yields
            Field schemas.
        """
        for index, field_data in enumerate(fields_data):
            yield Schema._make_field(index, field_data)

    @staticmethod
    def _make_field_map(fields):
        """Builds the field map.
        Guarantees field name unicity.
        Args:
            fields: iterable of field schema.
        Returns:
            A read-only map of field schemas, indexed by name.
        """
        field_map = {}
        for field in fields:
            if field.name in field_map:
                raise SchemaParseException(
                    "Duplicate record field name {0}.".format(field.name))
            field_map[field.name] = field
        return MappingProxyType(field_map)

    def __init__(self, name=None, output_format=None, output_rec_cnt=None, 
        source=None, seed=None, output_file=None, fields_data=None):
        # add members
        names = Names(name, output_format, output_rec_cnt, source, seed, output_file)
        fields = Schema._make_field_list(fields_data)
        self._props = {}
        self._props['names'] = self._names = names
        self._props['fields'] = self._fields = tuple(fields)
        field_map = Schema._make_field_map(self._fields)
        self._props['field_map'] = self._field_map = field_map

    # read-only properties
    @property
    def names(self):
        return self._names
    
    @property
    def fields(self):
        return self._fields
    
    @property
    def field_map(self):
        return self._field_map
    
    @property
    def props(self):
        return self._props

#
# Module Methods
#

def make_config_object(json_data):
    """Build Input Schema from data parsed out of JSON string."""
    
    #check if only valid named types are provided
    _validate_names_or_values(json_data.keys(), VALID_NAMED_TYPES)
    name = json_data.get('name')
    output_format = json_data.get('output_format')
    output_rec_cnt = json_data.get('output_rec_cnt')
    source = json_data.get('source')
    seed = json_data.get('seed')
    output_file = json_data.get('output_file')
    fields_data = json_data.get('fields')

    return Schema(name, output_format, output_rec_cnt, source, seed, output_file, fields_data)

def parse(input_schema_file):
    """Constructs the Schema from the JSON file."""
    # parse the JSON
    try:
        schema_file = open(input_schema_file,"r")
    except FileNotFoundError as e:
        raise FileNotFoundError("Provided input config file does not exist.")

    try:
        json_data = json.load(schema_file)
    except Exception as e:
        raise SchemaParseException("Exception {0} occured while parsing input schema".format(e))

    # construct the Schema object
    return make_config_object(json_data)