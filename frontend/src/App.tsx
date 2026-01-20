import { useState, useRef, useEffect } from 'react';
import './App.css'

const App = () => {
  const [values, setValues] = useState({ rpm: 0, tps: 0 });
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    ws.current = new WebSocket('ws://localhost:8000/ws');
    return () => ws.current?.close();
  }, []);

  const handleChange = (name: string, val: string) => {
    const newVal = parseInt(val)
    setValues(prev => ({ ...prev, [name]: newVal }));
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify({[name]: newVal}))
    }
  };

  const changeStatus = (status: 'start' | 'stop') => {
    fetch('http://localhost:8000/start-broadcast',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json', // CRITICAL
        },
        body: JSON.stringify({ status })
      }
    )
  }

  return (
    <div>
      <h1>MaxxECU Simulator</h1>

      <div>
        <section>
          <label>RPM: {values.rpm}</label>
          <input
            type="range" min="0" max="9000" step="50"
            value={values.rpm}
            onChange={(e) => handleChange('rpm', e.target.value)}
          />
        </section>

        <section>
          <label>Throttle (TPS): {values.tps}%</label>
          <input
            type="range" min="0" max="100"
            value={values.tps}
            onChange={(e) => handleChange('tps', e.target.value)}
          />
        </section>
        <button onClick={() => changeStatus('start')}>Start</button>
        <button onClick={() => changeStatus('stop')}>Stop</button>
      </div>
    </div>
  );
};


export default App;
