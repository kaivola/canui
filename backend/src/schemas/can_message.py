import can
from can import BusABC, ModifiableCyclicTaskABC
from cantools.database.can.message import Message as DbcMessage


class CanMessage:
    id: int
    dbc_entry: DbcMessage
    task: ModifiableCyclicTaskABC | None
    freq: int
    signal_values: dict[str, int | float]

    def __init__(self, dbc_entry: DbcMessage, freq: int = 1):
        self.dbc_entry = dbc_entry
        self.id = dbc_entry.frame_id
        self.freq = freq
        if dbc_entry.signal_tree is None:
            return
        self.signal_values = dict.fromkeys(
            [
                item
                for sublist in dbc_entry.signal_tree
                for item in (sublist if isinstance(sublist, list) else [sublist])
            ],
            0,
        )

    def start_send_periodic(self, bus: BusABC):
        task = bus.send_periodic(
            can.Message(
                arbitration_id=self.dbc_entry.frame_id,
                data=self.dbc_entry.encode(self.signal_values),
            ),
            period=1.0 / self.freq,
        )
        if isinstance(task, can.ModifiableCyclicTaskABC):
            self.task = task
        else:
            task.stop()
            raise TypeError(
                "The current CAN interface does not support modifiable tasks."
            )

    def update_signal(self, signal: str, new_value: int | float):
        if not hasattr(self, "task") or self.task is None:
            return
        msg = self.task.messages[0]
        decoded_data = self.dbc_entry.decode_simple(bytes(msg.data))
        print(f"value: {new_value}")
        decoded_data.update({signal: new_value})
        new_data = self.dbc_entry.encode(decoded_data)
        msg.data = bytearray(new_data)
        self.task.modify_data(msg)
        self.signal_values[signal] = new_value
