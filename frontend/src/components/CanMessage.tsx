import { Button, Card, Flex, Text } from "@radix-ui/themes";
import { memo } from "react";
import type { Message } from "../types/schema";
import { Signal } from "./Signal";

interface Props {
  message: Message;
  onSignalChange: (signalName: string, value: number) => void;
  changeVisibility: () => void;
}

export const CanMessage = memo(
  ({ message, onSignalChange, changeVisibility: onHideClick }: Props) => {
    return (
      <Card mb={"4"}>
        <Flex justify={"between"} mb={"4"}>
          <div>
            <Text size={"6"} mr={"4"}>
              {message.name}
            </Text>
          </div>
          <Button onClick={onHideClick}>
            {message.hidden ? "Enable" : "Disable"}
          </Button>
        </Flex>
        {!message.hidden &&
          Object.values(message.signals).map((signal) => (
            <Signal
              key={signal.name}
              signal={signal}
              onChange={onSignalChange}
            />
          ))}
      </Card>
    );
  },
);
