import { Button, Flex, Heading, Section } from "@radix-ui/themes";
import { useCallback, useEffect, useRef } from "react";
import { CanMessage } from "./components/CanMessage";
import { MessageFilter } from "./components/MessageFilter";
import { useMessages } from "./hooks/useMessages";
import { useStatus } from "./hooks/useStatus";
import { WEBSOCKET_URL } from "./utils/constants";

const App = () => {
  const ws = useRef<WebSocket | null>(null);
  const timerRef = useRef<number | null>(null);

  const { messages, changeVisibility, updateSignalValue } = useMessages();
  const { isTransmitting, changeStatus } = useStatus();

  useEffect(() => {
    ws.current = new WebSocket(WEBSOCKET_URL + "/can-data");
    return () => ws.current?.close();
  }, []);

  const handleChange = useCallback(
    (messageId: number) => {
      return (signalName: string, value: number) => {
        updateSignalValue(messageId, signalName, value);

        if (timerRef.current) clearTimeout(timerRef.current);

        timerRef.current = setTimeout(() => {
          if (ws.current?.readyState === WebSocket.OPEN) {
            ws.current.send(JSON.stringify({ messageId, signalName, value }));
          }
        }, 50);
      };
    },
    [updateSignalValue],
  );

  return (
    <div>
      <Section px={"4"}>
        <Flex justify={"between"}>
          <Heading>Can Simulator</Heading>
          <Button
            onClick={() => changeStatus(isTransmitting ? "stop" : "start")}
          >
            {isTransmitting ? "stop" : "start"}
          </Button>
        </Flex>
      </Section>
      <Section px={"4"}>
        <MessageFilter
          messages={messages}
          changeVisibility={changeVisibility}
        />
        <div style={{ columnCount: 2, columnGap: "4 rem" }}>
          {Boolean(Object.keys(messages).length) &&
            Object.values(messages)
              .filter((m) => !m.hidden)
              .map((message) => (
                <CanMessage
                  key={message.id}
                  message={message}
                  changeVisibility={() => changeVisibility(message.id)}
                  onSignalChange={handleChange(message.id)}
                />
              ))}
        </div>
      </Section>
    </div>
  );
};

export default App;
