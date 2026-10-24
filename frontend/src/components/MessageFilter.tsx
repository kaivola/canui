import { Button, DropdownMenu } from "@radix-ui/themes";
import { useMemo } from "react";
import type { Message } from "../types/schema";

type MessageFilterProps = {
  messages: Record<number, Message>;
  toggleMessage: (messageId: number, enable: boolean) => void;
};

export const MessageFilter = ({
  messages,
  toggleMessage,
}: MessageFilterProps) => {
  const messageCount = useMemo(() => {
    const m = Object.values(messages);
    return `${m.length - m.reduce((sum, message) => (message.hidden ? sum + 1 : sum), 0)}/${m.length}`;
  }, [messages]);

  return (
    <DropdownMenu.Root>
      <DropdownMenu.Trigger>
        <Button mb={"4"}>Messages {messageCount}</Button>
      </DropdownMenu.Trigger>

      <DropdownMenu.Content sideOffset={8}>
        <DropdownMenu.Label>Messages</DropdownMenu.Label>
        {Object.values(messages).map((m) => (
          <DropdownMenu.CheckboxItem
            key={m.id}
            checked={!m.hidden}
            onCheckedChange={(enable) => toggleMessage(m.id, enable)}
          >
            {m.id}
          </DropdownMenu.CheckboxItem>
        ))}
      </DropdownMenu.Content>
    </DropdownMenu.Root>
  );
};
