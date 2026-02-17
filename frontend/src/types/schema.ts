import type { components } from "./api";

type SignalDto = components['schemas']['SignalDto']

export type Message = {
    id: number
    signals: Signal[]
}
export type Signal = SignalDto & {
    value: number
}
