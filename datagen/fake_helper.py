from faker import Faker
from datetime import datetime
import re

ADDRESS_FORMAT = re.compile(r'(.*)\\n(.*),?\s+(.*)\s+([\d]*)')
class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class FakeHelper:
    """This Class is used to generate fake data."""
    def __init__(self, num_records=1000,seed=1000):
        self.num_records = num_records
        self.faker = Faker()
        self.seed = seed
    
    def _fake_address(self):
        return ADDRESS_FORMAT.match(repr(self.faker.address())).group
    
    def _fake_boolean(self):
        return self.faker.pybool()

    def _faker_currency(self):
        return self.faker.currency()
    
    def _fake_date(self, min_value, max_value):
        if min_value is None:
            date_start = datetime.strptime("1970-01-01", "%Y-%m-%d")
        else:
            date_start = datetime.strptime(min_value, "%Y-%m-%d")
        if max_value is None:
            date_end = datetime.now()
        else:
            date_end = datetime.strptime(max_value, "%Y-%m-%d")
        return self.faker.date_between_dates(date_start=date_start, date_end=date_end)
    
    def _fake_date_time(self, min_value, max_value):
        if min_value is None:
            start_time = '-30y'
        else:
            start_time = datetime.strptime(min_value, "%Y-%m-%d %H:%M:%S")
        if max_value is None:
            end_time = 'now'
        else:
            end_time = datetime.strptime(max_value, "%Y-%m-%d %H:%M:%S")
        return self.faker.date_time_between(start_date=start_time, end_date=end_time)
    
    def _fake_decimal(self, min_value, max_value):
        return self.faker.pydecimal(min_value=min_value, max_value=max_value)
    
    def _fake_float(self, min_value, max_value):
        return self.faker.pyfloat(min_value=min_value, max_value=max_value)
    
    def _fake_int(self, min_value, max_value):

        if min_value is None:
            min_value = 0
        if max_value is None:
            max_value = 999
        return self.faker.pyint(min_value=min_value, max_value=max_value)
    
    def _fake_lorem(self, max_length):
        if max_length is None:
            max_length = 3
        return self.faker.paragraph(nb_sentences=max_length)
    
    def _fake_str(self, min_length, max_length, format):
        
        if format is None:
            if max_length is None:
                max_length = 20
            return self.faker.pystr(min_chars=min_length, max_chars=max_length)
        else:
            return self.faker.bothify(format)
    
    def fake_it(self, data_type, min_length=None, max_length=None,
        min_value=None, max_value=None, format=None, values=None):
        Faker.seed(self.seed)
        return_list = list()
        status = True
        try:
            for _ in range(self.num_records):
                if data_type.lower() == "address":
                    #return_list.append(self._fake_address()(0))
                    return_list.append(self.faker.address())
                elif data_type.lower() == "boolean":
                    return_list.append(self._fake_boolean())
                elif data_type.lower() == "cat":
                    return_list.append(self.faker.random_element(elements=values))
                elif data_type.lower() == "city":
                    #return_list.append(self._fake_address()(2))
                    return_list.append(self.faker.city())
                elif data_type.lower() == "country":
                    return_list.append(self.faker.country())
                elif data_type.lower() == "currency_code":
                    return_list.append(self._faker_currency()(0))
                elif data_type.lower() == "currency_name":
                    return_list.append(self._faker_currency()(1))
                elif data_type.lower() == "date":
                    return_list.append(self._fake_date(min_value, max_value))
                elif data_type.lower() in ("decimal", "double"):
                    return_list.append(self._fake_decimal(min_value, max_value))
                elif data_type.lower() == "first_name":
                    return_list.append(self.faker.first_name())
                elif data_type.lower() == "float":
                    return_list.append(self._fake_float(min_value, max_value))
                elif data_type.lower() == "int":
                    return_list.append(self._fake_int(min_value, max_value))
                elif data_type.lower() == "job":
                    return_list.append(self.faker.job())
                elif data_type.lower() == "last_name":
                    return_list.append(self.faker.last_name())
                elif data_type.lower() == "lorem":
                    return_list.append(self._fake_lorem(max_length))
                elif data_type.lower() == "name":
                    return_list.append(self.faker.name())
                elif data_type.lower() == "state":
                    #return_list.append(self._fake_address()(3))
                    return_list.append(self.faker.state())
                elif data_type.lower() == "street_address":
                    #return_list.append(self._fake_address()(1))
                    return_list.append(self.faker.street_address())
                elif data_type.lower() in ("string", "str"):
                    return_list.append(self._fake_str(min_length, max_length, format))
                elif data_type.lower() == "time":
                    return_list.append(self.faker.time())
                elif data_type.lower() == "timestamp":
                    return_list.append(self._fake_date_time(min_value, max_value))
                elif data_type.lower() == "zip_code":
                    #return_list.append(self._fake_address()(4))
                    return_list.append(self.faker.postcode())
                else:
                    return_list.append(None)
        except Exception as e:
            status = False
            raise Error("Cann't fake data_type: {0}, Exception {1} occurred.".format(data_type, e))
        return (status, return_list)