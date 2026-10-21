import type { components } from "./api";

export type SignalDto = components["schemas"]["SignalDto"];
export type MessageDto = components["schemas"]["MessageDto"];

export type Message = Omit<MessageDto, "signals"> & {
  hidden: boolean;
  signals: Record<string, Signal>;
};
export type Signal = SignalDto & {
  value: number;
};
