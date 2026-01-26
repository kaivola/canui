import can
from can import BusABC, ModifiableCyclicTaskABC
from cantools.database.can.message import Message as DbcMessage


class CanMessage:
    id: int
    dbc_entry: DbcMessage
    task: ModifiableCyclicTaskABC | None
    signals: set[str]

    def __init__(self, dbc_entry: DbcMessage):
        self.dbc_entry = dbc_entry
        self.id = dbc_entry.frame_id
        self.signals = set(dbc_entry.signal_tree)
        dbc_entry.signals

    def createTaskWithEmptyData(self, bus: BusABC, freq: int):
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

    def createTaskFromData(self, bus: BusABC, freq: int, data: dict[str, int]):
        extra_signals = data.keys() - self.signals
        if extra_signals:
            print(f"Invalid signals: {extra_signals}")
        msg_data = self.dbc_entry.encode(data)
        self.task = bus.send_periodic(
            can.Message(arbitration_id=self.id, data=msg_data),
            period=1.0 / freq,
            autostart=False,
        )

    def update_data(self, data):
        if not (isinstance(self.task, ModifiableCyclicTaskABC)):
            return

        new_data = self.dbc_entry.encode(data)

        self.task.modify_data(
            can.Message(
                arbitration_id=self.id,
                data=new_data,
            )
        )
