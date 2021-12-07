from src.helpers import register_command
from src.validators import String


# echo command

class EchoCommandData:
    text = String(minsize=0, maxsize=666)

    def __init__(self, *args):
        assert len(args) == 1, '"echo" command takes exactly 1 argument'
        self.text = args[0]


@register_command
def echo(*args):
    echo_data = EchoCommandData(*args)
    return echo_data.text
