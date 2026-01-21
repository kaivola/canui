import { useState, useRef, useEffect } from 'react';
import './App.css'

const App = () => {
  const [isBroadcasting, setIsBroadcasting] = useState(false)
  const [values, setValues] = useState({ rpm: 0, tps: 0 });
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    fetch('http://localhost:8000/status')
      .then(res => {
        return res.json()
      })
      .then(json => {
        setIsBroadcasting(json.isBroadcasting)
      })
    ws.current = new WebSocket('ws://localhost:8000/ws');
    return () => ws.current?.close();
  }, []);

  const handleChange = (name: string, val: string) => {
    const newVal = parseInt(val)
    setValues(prev => ({ ...prev, [name]: newVal }));
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify({ [name]: newVal }))
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
        {isBroadcasting ? (
          <button onClick={() => changeStatus('stop')}>Stop</button>
        ) : (
          <button onClick={() => changeStatus('start')}>Start</button>
        )}
      </div>
    </div>
  );
};


export default App;
