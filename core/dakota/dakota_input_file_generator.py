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
        for i, k in enumerate(self.content):
            # print(k)
            if type(k) == dict:
                for keyword in k:
                    print(keyword)
                    result += "{indent}{0}\n".format(keyword, indent=0*" ")
                    result += self.dict_to_string(self.content[i][keyword])
            result += '\n'

        return result

    def dict_to_string(self, data, indent=3):
        string = ""

        for keyword in data:
            if type(data[keyword]) == str and data[keyword] == '':
                string += "{indent}{0}{1}\n".format(keyword, data[keyword], indent=indent*" ")
            elif type(data[keyword]) == str:
                string += "{indent}{0} = '{1}'\n".format(keyword, data[keyword], indent=indent*" ")
            elif type(data[keyword]) in [int, float]:
                string += "{indent}{0} = {1}\n".format(keyword, data[keyword], indent=indent*" ")
            elif type(data[keyword]) == list:
                list_string = ""
                for i in data[keyword]:
                    if type(i) in [int, float]:
                        list_string += str(i) + "    "
                    elif type(i) == str:
                        list_string += "'" + str(i) + "'" + "    "
                string += "{indent}{0}     {1}\n".format(keyword, list_string, indent=indent*" ")
            else:
                string += "{indent}{0} {1}\n".format(keyword, data[keyword], indent=indent*" ")

        return string




