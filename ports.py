from typing import List, Union

MAX_PORT = 65535

class InvalidPortDefinitionError(Exception):
    pass


class PortRange:
    """Subclass for representation of port ranges"""

    def __init__(self, user_input_ports: List[Union[str, int]]):
        self.input_ports = user_input_ports
        self._base_range = [0] * (MAX_PORT + 2)
        self.create_ranges()

    def create_ranges(self):
        for input_port_range in self.input_ports:
            range_start, range_end = self.process_port_input(input_port_range)
            self._base_range[range_start] += 1
            self._base_range[range_end] -= 1

    def process_port_input(self, input_port):
        try:
            range_start = int(input_port)
            range_end = range_start + 1
        except ValueError:
            try:
                left_num, right_num = input_port.split("-")
                range_start = int(left_num)
                range_end = int(right_num) + 1
            except ValueError:
                raise InvalidPortDefinitionError(f"Invalid port range definition format")
        if not ((0 < range_start <= (MAX_PORT + 1)) and (0 < range_end <= (MAX_PORT + 1)) and (range_start < range_end)):
            raise InvalidPortDefinitionError("Ports are out of range")

        return range_start, range_end

    def __repr__(self):
        repr_str = ""
        range_start_indicator, i = 0, 0
        while i < len(self._base_range):
            range_start_indicator += self._base_range[i]
            if range_start_indicator < 0:
                range_start_indicator = 0
            left_port = i
            while range_start_indicator > 0 and i <= len(self._base_range):
                i += 1
                range_start_indicator += self._base_range[i]
            right_port = i
            if right_port != left_port:
                if left_port == right_port - 1:
                    repr_str += f" {left_port}"
                else:
                    repr_str += f" {left_port}-{right_port-1}"
            i += 1
        return f"[{repr_str}]"


input_ports = [8000, '9000-9100', '9050-9150', '100-202', '100-201', '65530-65535', '1-2']

pr = PortRange(input_ports)
print(pr)
