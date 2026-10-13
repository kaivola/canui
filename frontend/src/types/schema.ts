import type { components } from "./api";

type SignalDto = components['schemas']['SignalDto']
type MessageDto = components['schemas']['MessageDto']

export type Message = Omit<MessageDto, 'signals'> & {
    hidden: boolean
    signals: Signal[]
}
export type Signal = SignalDto & {
    displayName: string
    value: number
}
