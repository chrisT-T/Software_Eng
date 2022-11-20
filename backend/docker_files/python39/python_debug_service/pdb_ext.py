import inspect
import os
from pdb import Pdb
from pprint import pformat


class PdbExt(Pdb):
    def __init__(self, stdin, stdout):
        PdbExt.instance = self
        super().__init__(stdin=stdin, stdout=stdout)

    def get_current_stack(self):
        res = []
        for s in self.stack:
            res.append(s[0].__str__())
        return res

    def get_current_function(self):
        return self.curframe.f_code.co_name

    def get_repr_value(self, repr):
        try:
            return {'value': self._getval(repr), 'runflag': True}
        except: # noqa
            return {'runflag': False}

    def get_current_frame_data(self):
        try:
            filename = self.curframe.f_code.co_filename
            lines, start_line = inspect.findsource(self.curframe)
            res = {
                'dirname': os.path.dirname(os.path.abspath(filename)) + os.path.sep,
                'filename': os.path.basename(filename),
                'rawfilename': filename.replace(os.getcwd(), '.', 1),
                'file_listing': ''.join(lines),
                'current_line': self.curframe.f_lineno,
                'breakpoints': self.get_file_breaks(filename),
                'globals': self.get_globals(),
                'locals': self.get_locals()
            }
        except: # noqa
            res = 'null frame data'
        return res

    """
    The following three functions comes from the project: web-pdb
    https://pypi.org/project/web-pdb
    """

    def _format_variables(self, raw_vars):
        """
        :param raw_vars: a `dict` of `var_name: var_object` pairs
        :type raw_vars: dict
        :return: sorted list of variables as a unicode string
        :rtype: unicode
        """
        f_vars = []
        for var, value in raw_vars.items():
            if not (var.startswith('__') and var.endswith('__')):
                repr_value = self._get_repr(value)
                f_vars.append('{0} = {1}'.format(var, repr_value))
        return '\n'.join(sorted(f_vars))

    def get_globals(self):
        """
        Get the listing of global variables in the current scope
        .. note:: special variables that start and end with
            double underscores ``__`` are not included.
        :return: a listing of ``var = value`` pairs sorted alphabetically
        :rtype: unicode
        """
        return self._format_variables(self.curframe.f_globals)

    def get_locals(self):
        """
        Get the listing of local variables in the current scope
        .. note:: special variables that start and end with
            double underscores ``__`` are not included.
            For module scope globals and locals listings are the same.
        :return: a listing of ``var = value`` pairs sorted alphabetically
        :rtype: unicode
        """
        return self._format_variables(self.curframe_locals)

    @staticmethod
    def _get_repr(obj, pretty=False, indent=1):
        """
        Get string representation of an object
        :param obj: object
        :type obj: object
        :param pretty: use pretty formatting
        :type pretty: bool
        :param indent: indentation for pretty formatting
        :type indent: int
        :return: string representation
        :rtype: str
        """
        if pretty:
            pformat(obj, indent)
        else:
            repr(obj)
        return
