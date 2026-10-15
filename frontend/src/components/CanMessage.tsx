import { Button, Card, Flex, Text } from "@radix-ui/themes";
import type { Message } from "../types/schema";
import { Signal } from "./Signal";
import { memo } from "react";

interface Props {
  message: Message;
  onSignalChange: (signalName: string, value: number) => void;
  changeVisibility: () => void;
}

export const CanMessage = memo(({ message, onSignalChange, changeVisibility: onHideClick }: Props) => {
  return (
    <Card mb={'4'}>
      <Flex justify={"between"} mb={"4"}>
        <Text size={"8"}>{message.id}</Text>
        <Button onClick={onHideClick}>{message.hidden ? "Show" : "Hide"}</Button>
      </Flex>
      {!message.hidden &&
        Object.values(message.signals).map((signal) => (
          <Signal key={signal.name} signal={signal} onChange={onSignalChange} />
        ))}
    </Card>
  );
});
