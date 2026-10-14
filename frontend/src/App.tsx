import { useState, useRef, useEffect } from "react";
import type { Message } from "./types/schema";
import { Button, Flex, Heading, Section } from "@radix-ui/themes";
import { CanMessage } from "./components/CanMessage";
import { dbcSignals } from "./utils/signals";

const App = () => {
  const [isBroadcasting, setIsBroadcasting] = useState(false);
  const [messages, setMessages] = useState<Record<number, Message>>([]);
  const ws = useRef<WebSocket | null>(null);
  const timerRef = useRef<number | null>(null);

  useEffect(() => {
    fetch("http://localhost:8000/status")
      .then((res) => {
        return res.json();
      })
      .then((json) => {
        setIsBroadcasting(json.isBroadcasting);
      })
      .catch((e) => console.error(e));

    ws.current = new WebSocket("ws://localhost:8000/can-data");
    return () => ws.current?.close();
  }, []);

  useEffect(() => {
    fetch("http://localhost:8000/messages")
      .then((res) => res.json())
      .then((data: Message[]) => {
        setMessages(
          data.reduce(
            (prev, curr) => {
              prev[curr.id] = {
                ...curr,
                signals: curr.signals.map((s) => ({ ...s, displayName: dbcSignals[curr.id][s.name] })),
              };
              return prev;
            },
            {} as Record<number, Message>,
          ),
        );
      })
      .catch((e) => console.error(e));
  }, []);

  const handleChange = (messageId: number) => (signalName: string) => (value: number) => {
    // console.log("messageId", messageId, "signalName", signalName, "value", value);
    setMessages((prevMessages) => {
      const m = prevMessages[messageId];
      if (!m) return prevMessages;
      return {
        ...prevMessages,
        [messageId]: {
          ...m,
          signals: m.signals.map((s) => (s.name === signalName ? { ...s, value } : s)),
        },
      };
    });

    if (timerRef.current) clearTimeout(timerRef.current);

    timerRef.current = setTimeout(() => {
      if (ws.current?.readyState === WebSocket.OPEN) {
        ws.current.send(JSON.stringify({ messageId, signalName, value }));
      }
    }, 50);
  };

  const changeStatus = (status: "start" | "stop") => {
    fetch("http://localhost:8000/status", {
      method: "put",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ status }),
    })
      .then((res) => res.json())
      .then((json) => setIsBroadcasting(json.isBroadcasting))
      .catch((e) => console.error(e));
  };

  const changeVisibility = (id: number) => {
    setMessages((prevMessages) => {
      const m = prevMessages[id]
      return {
      ...prevMessages,
      [id]: {
        ...m,
        hidden: !m.hidden,
      },
      }
    });
  };

  return (
    <div>
      <Section px={"4"}>
        <Flex justify={"between"}>
          <Heading>Can Simulator</Heading>
          <Button onClick={() => changeStatus(isBroadcasting ? "stop" : "start")}>
            {isBroadcasting ? "stop" : "start"}
          </Button>
        </Flex>
      </Section>
      <div style={{ columnCount: 2, columnGap: "4 rem" }}>
        {Boolean(Object.keys(messages).length) &&
          Object.values(messages).map((message) => (
            <CanMessage
              key={message.id}
              message={message}
              changeVisibility={() => changeVisibility(message.id)}
              onSignalChange={handleChange(message.id)}
            />
          ))}
      </div>
    </div>
  );
};

export default App;
