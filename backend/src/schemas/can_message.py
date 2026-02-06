import can
from can import BusABC, ModifiableCyclicTaskABC
from cantools.database.can.message import Message as DbcMessage


class CanMessage:
    id: int
    dbc_entry: DbcMessage
    task: ModifiableCyclicTaskABC | None
    freq: int
    signal_values: dict[str, int]

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

    def update_signal(self, signal: str, data: int):
        if not hasattr(self, "task") or self.task is None:
            return
        msg = self.task.messages[0]
        old_decoded = self.dbc_entry.decode_simple(msg.data)
        old_decoded.update({signal: data})
        new_data = self.dbc_entry.encode(old_decoded)
        msg.data = bytearray(new_data)
        self.task.modify_data(msg)
