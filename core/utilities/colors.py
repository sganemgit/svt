class colors(object):
    _reset='\033[0m'
    _bold='\033[01m'
    _disable='\033[02m'
    _underline='\033[04m'
    _reverse='\033[07m'
    _strikethrough='\033[09m'
    _invisible='\033[08m'
    #font colors
    _black='\033[30m'
    _red='\033[31m'
    _green='\033[32m'
    _orange='\033[33m'
    _blue='\033[34m'
    _purple='\033[35m'
    _cyan='\033[36m'
    _lightgrey='\033[37m'
    _darkgrey='\033[90m'
    _lightred='\033[91m'
    _lightgreen='\033[92m'
    _yellow='\033[93m'
    _lightblue='\033[94m'
    _pink='\033[95m'
    _lightcyan='\033[96m'
    #background colors
    _black_bg='\033[40m'
    _red_bg='\033[41m'
    _green_bg='\033[42m'
    _orange_bg='\033[43m'
    _blue_bg='\033[44m'
    _purple_bg='\033[45m'
    _cyan_bg='\033[46m'
    _lightgrey_bg='\033[47m'

    @classmethod
    def Red(cls, msg):
        return cls._red+msg+cls._reset

    @classmethod
    def Green(cls, msg):
        return cls._green+msg+cls._reset

    @classmethod
    def Blue(cls, msg):
        return cls._blue+msg+cls._reset

    @classmethod
    def Orange(cls,msg):
        return cls._orange+msg+cls._reset

    @classmethod
    def GreenBG(cls, msg):
        return cls._green_bg+msg+cls._reset
