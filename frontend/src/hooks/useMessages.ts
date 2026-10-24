import { useState } from "react";
import type { Message, MessageDto } from "../types/schema";
import { BACKEND_URL } from "../utils/constants";

type Messages = Record<number, Message>;

const mapMessageData = (data: MessageDto[]): Messages => {
  const messagesRecord: Messages = {};

  for (const message of data) {
    const signalsRecord = Object.fromEntries(
      message.signals.map((signal) => [signal.name, signal]),
    );

    messagesRecord[message.id] = {
      ...message,
      signals: signalsRecord,
      hidden: false,
    };
  }

  return messagesRecord;
};

export const useMessages = () => {
  const [messages, setMessages] = useState<Messages>([]);

  const updateSignalValue = (
    messageId: number,
    signalName: string,
    value: number,
  ) => {
    setMessages((prevMessages) => {
      const targetMessage = prevMessages[messageId];
      if (!targetMessage) return prevMessages;

      return {
        ...prevMessages,
        [messageId]: {
          ...targetMessage,
          signals: {
            ...targetMessage.signals,
            [signalName]: {
              ...targetMessage.signals[signalName],
              value,
            },
          },
        },
      };
    });
  };

  const changeVisibility = (messageId: number) => {
    fetch(BACKEND_URL + `/messages/${messageId}`)
      .then(() =>
        setMessages((prevMessages) => {
          const m = prevMessages[messageId];
          return {
            ...prevMessages,
            [messageId]: {
              ...m,
              hidden: !m.hidden,
            },
          };
        }),
      )
      .catch(console.error);
  };

  const updateMessages = (data: MessageDto[]) =>
    setMessages(mapMessageData(data));

  return { messages, updateMessages, changeVisibility, updateSignalValue };
};
