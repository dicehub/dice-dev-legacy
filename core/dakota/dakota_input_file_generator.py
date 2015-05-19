# Standard Python modules
# =======================
from collections import OrderedDict


class DakotaInputFileGenerator:

    def __init__(self, content):

        self.content = content

    def make_string(self):
        """
        turns data into a string
        """

        result = ""

        # First level (Main blocks: 'environment, model, interface, ...')
        # ===============================================================
        for k in self.content:
            if type(self.content[k]) == OrderedDict:
                result += "{indent}{0}{1}\n".format(k, self.content[k]['value'], indent=0*" ")
                result += self.dict_to_string(self.content[k]['child'])
            result += '\n'

        return result

    def dict_to_string(self, data, indent=3):
        string = ""

        for keyword in data:
            if type(data[keyword]['value']) == str and data[keyword]['value'] == '':
                string += "{indent}{0}{1}\n".format(keyword, data[keyword]['value'], indent=indent*" ")
            elif type(data[keyword]['value']) == str:
                string += "{indent}{0} = '{1}'\n".format(keyword, data[keyword]['value'], indent=indent*" ")
            elif type(data[keyword]['value']) in [int, float]:
                string += "{indent}{0} = {1}\n".format(keyword, data[keyword]['value'], indent=indent*" ")
            elif type(data[keyword]['value']) == list:
                list_string = ""
                for i in data[keyword]['value']:
                    if type(i) in [int, float]:
                        list_string += str(i) + "    "
                    elif type(i) == str:
                        list_string += "'" + str(i) + "'" + "    "
                string += "{indent}{0}     {1}\n".format(keyword, list_string, indent=indent*" ")
            else:
                string += "{indent}{0} {1}\n".format(keyword, data[keyword]['value'], indent=indent*" ")
            if 'child' in data[keyword]:
                string += self.dict_to_string(data[keyword]['child'], indent*2)

        return string




