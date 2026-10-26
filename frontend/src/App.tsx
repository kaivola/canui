import { Button, Flex, Heading, Section, Select } from "@radix-ui/themes";
import { useCallback, useEffect, useRef, useState } from "react";
import { CanMessage } from "./components/CanMessage";
import { MessageFilter } from "./components/MessageFilter";
import { useMessages } from "./hooks/useMessages";
import { useStatus } from "./hooks/useStatus";
import { BACKEND_URL, WEBSOCKET_URL } from "./utils/constants";

const App = () => {
  const ws = useRef<WebSocket | null>(null);
  const timerRef = useRef<number | null>(null);
  const [files, setFiles] = useState<string[]>([]);

  const { messages, updateMessages, toggleMessage, updateSignalValue } =
    useMessages();
  const { isTransmitting, changeStatus } = useStatus();

  useEffect(() => {
    fetch(BACKEND_URL + "/messages/dbc-files")
      .then((res) => res.json())
      .then(setFiles)
      .catch(console.error);
    return () => ws.current?.close();
  }, []);

  const handleSignalValueChange = useCallback(
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

  const handleFileChange = (filename: string) => {
    if (filename.trim().length > 0) {
      fetch(`${BACKEND_URL}/messages/dbc-files/${filename}`, { method: "POST" })
        .then((res) => res.json())
        .then((messages) => {
          ws.current?.close();
          ws.current = new WebSocket(WEBSOCKET_URL + "/can-data");
          updateMessages(messages);
        })
        .catch(console.error);
    }
  };

  return (
    <div>
      <Section px={"8"}>
        <Flex justify={"between"}>
          <Heading size={"8"}>
            can<span style={{ color: "var(--accent-10)" }}>ui</span>
          </Heading>
          <Button
            onClick={() => changeStatus(isTransmitting ? "stop" : "start")}
          >
            {isTransmitting ? "stop" : "start"}
          </Button>
        </Flex>
      </Section>
      <Section px={"8"}>
        <Flex gap={"4"}>
          <Select.Root onValueChange={handleFileChange}>
            <Select.Trigger placeholder="Select dbc file" />
            <Select.Content position="popper">
              <Select.Item value={"Select file"} disabled>
                Select file
              </Select.Item>
              {files.map((f) => (
                <Select.Item key={f} value={f}>
                  {f}
                </Select.Item>
              ))}
            </Select.Content>
          </Select.Root>
          <MessageFilter messages={messages} toggleMessage={toggleMessage} />
        </Flex>
        <div style={{ columnCount: 2, columnGap: "4 rem" }}>
          {Boolean(Object.keys(messages).length) &&
            Object.values(messages)
              .filter((m) => !m.hidden)
              .map((message) => (
                <CanMessage
                  key={message.id}
                  message={message}
                  changeVisibility={() => toggleMessage(message.id, false)}
                  onSignalChange={handleSignalValueChange(message.id)}
                />
              ))}
        </div>
      </Section>
    </div>
  );
};

export default App;
