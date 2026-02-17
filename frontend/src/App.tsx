import { useState, useRef, useEffect } from 'react';
import type { Message } from './types/schema';
import { Container, Grid, Section } from '@radix-ui/themes';
import { CanMessage } from './components/CanMessage';

const App = () => {
  const [isBroadcasting, setIsBroadcasting] = useState(false)
  const [messages, setMessages] = useState<Message[]>([])
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    fetch('http://localhost:8000/status')
      .then(res => {
        return res.json()
      })
      .then(json => {
        setIsBroadcasting(json.isBroadcasting)
      })
    ws.current = new WebSocket('ws://localhost:8000/can-data');
    return () => ws.current?.close();
  }, []);

  useEffect(() => {
    fetch('http://localhost:8000/messages')
      .then(res => res.json())
      .then((data: Message[]) => {
        setMessages(data)
        console.log('data', data)
      })
  }, [])

  const handleChange = (messageId: number) => (signalName: string) => (value: number) => {
    console.log('messageId', messageId, 'signalName', signalName, 'value', value)
    setMessages(prevMessages =>
      prevMessages.map(m => {
        if (m.id !== messageId) return m
        return {
          ...m,
          signals: m.signals.map(s =>
            s.name === signalName
              ? { ...s, value }
              : s
          )
        };
      })
    )
    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify({ messageId, signalName, value }))
    }
  };

  const changeStatus = (status: 'start' | 'stop') => {
    fetch('http://localhost:8000/status',
      {
        method: 'put',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status })
      }
    )
      .then(res => res.json())
      .then(json => setIsBroadcasting(json.isBroadcasting))
  }

  return (
    <Container height={"100%"}>
      <Grid columns={'2'}>
        {messages?.length && messages.toSorted((a, b) => a.id - b.id).map(message => (
          <CanMessage key={message.id} message={message} onSignalChange={handleChange(message.id)} />
        ))}
      </Grid>
      <Section>
        {isBroadcasting ? (
          <button onClick={() => changeStatus('stop')}>Stop</button>
        ) : (
          <button onClick={() => changeStatus('start')}>Start</button>
        )}
      </Section>
    </Container>
  );
};


export default App;
