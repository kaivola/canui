import can
from can import BusABC, ModifiableCyclicTaskABC
from cantools.database.can.message import Message as DbcMessage


class CanMessage:
    id: int
    dbc_entry: DbcMessage
    task: ModifiableCyclicTaskABC | None
    freq: int
    signals: set[str]

    def __init__(self, dbc_entry: DbcMessage, bus: BusABC, freq: int = 1):
        self.dbc_entry = dbc_entry
        self.id = dbc_entry.frame_id
        self.signals = set(dbc_entry.signal_tree)
        self.freq = freq
        self.task = bus.send_periodic(
            can.Message(
                arbitration_id=self.id,
            ),
            period=1.0 / freq,
            autostart=False,
        )

    def update_signal(self, signal: str, data: int):
        # old_data = self.task.messages[0].data
        # old_decoded = self.dbc_entry.decode(old_data)
        # new_data = old_decoded.update(signal, data)
        # TODO implement signal update
        pass
