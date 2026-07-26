const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, '..', 'frontend')));

const materiales = [
  { id: 1, nombre: 'Sensor ultrasónico HC-SR04', descripcion: 'Sensor de distancia con emisor y receptor ultrasónico.', cantidad: 1, uso: 'Medición de distancia' },
  { id: 2, nombre: 'Arduino Uno', descripcion: 'Placa de desarrollo con ATmega328P.', cantidad: 1, uso: 'Procesamiento y control' },
  { id: 3, nombre: 'Módulo L298N', descripcion: 'Controlador de motores DC.', cantidad: 1, uso: 'Drive de motor' },
  { id: 4, nombre: 'Motores DC con ruedas', descripcion: 'Motores eléctricos con ruedas amarillas.', cantidad: 2, uso: 'Locomoción' },
  { id: 5, nombre: 'Baterías AA (4 unidades)', descripcion: 'Fuente de energía 6V para el robot.', cantidad: 4, uso: 'Alimentación' },
  { id: 6, nombre: 'Protoboard y cables jumper', descripcion: 'Placa de conexiones y cables multicolores.', cantidad: 1, uso: 'Interconexión' }
];

let comentarios = [];

app.get('/api/materiales', (req, res) => {
  res.json(materiales);
});

app.post('/api/comentarios', (req, res) => {
  const { nombre, email, sensacion, comentario } = req.body;
  if (!nombre || !email || !sensacion || !comentario) {
    return res.status(400).json({ error: 'Faltan datos obligatorios.' });
  }

  const nuevoComentario = {
    id: comentarios.length + 1,
    nombre,
    email,
    sensacion,
    comentario,
    fecha: new Date().toISOString()
  };

  comentarios.push(nuevoComentario);
  res.status(201).json(nuevoComentario);
});

app.get('/api/comentarios', (req, res) => {
  res.json(comentarios);
});

app.listen(port, () => {
  console.log(`Backend iniciado en http://localhost:${port}`);
});
