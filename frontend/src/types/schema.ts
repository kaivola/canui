import type { components } from "./api";

type SignalDto = components['schemas']['SignalDto']

export type Message = {
    id: number
    signals: Signal[]
    hidden: boolean
}
export type Signal = SignalDto & {
    value: number
}
