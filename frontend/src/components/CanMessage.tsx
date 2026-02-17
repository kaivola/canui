import { Flex } from "@radix-ui/themes"
import type { Message } from "../types/schema"
import { Signal } from "./Signal"

interface Props {
    message: Message
    onSignalChange: (signalName: string) => (value: number) => void;
}

export const CanMessage = ({ message, onSignalChange }: Props) => {

    return (
        <Flex direction={'column'} gap={"1"} style={{ backgroundColor: "var(--gray-a2)", borderRadius: "var(--radius-3)" }}>
            {message.signals.map(signal => (
                <Signal key={signal.name} signal={signal} onChange={onSignalChange(signal.name)} />
            ))}
        </Flex>
    )
}