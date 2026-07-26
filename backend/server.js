const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');
const sql = require('mssql');

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, '..', 'frontend')));

const STATIC_MATERIALES = [
  { id: 1, nombre: 'Sensor ultrasónico HC-SR04', descripcion: 'Sensor de distancia con emisor y receptor ultrasónico.', cantidad: 1, uso: 'Medición de distancia' },
  { id: 2, nombre: 'Arduino Uno', descripcion: 'Placa de desarrollo con ATmega328P.', cantidad: 1, uso: 'Procesamiento y control' },
  { id: 3, nombre: 'Módulo L298N', descripcion: 'Controlador de motores DC.', cantidad: 1, uso: 'Drive de motor' },
  { id: 4, nombre: 'Motores DC con ruedas', descripcion: 'Motores eléctricos con ruedas amarillas.', cantidad: 2, uso: 'Locomoción' },
  { id: 5, nombre: 'Baterías AA (4 unidades)', descripcion: 'Fuente de energía 6V para el robot.', cantidad: 4, uso: 'Alimentación' },
  { id: 6, nombre: 'Protoboard y cables jumper', descripcion: 'Placa de conexiones y cables multicolores.', cantidad: 1, uso: 'Interconexión' }
];

const dbConfig = {
  user: process.env.DB_USER || 'sa',
  password: process.env.DB_PASSWORD || 'YourStrong!Passw0rd',
  server: process.env.DB_HOST || 'db',
  database: process.env.DB_NAME || 'proyectointerdisciplinar',
  port: parseInt(process.env.DB_PORT, 10) || 1433,
  options: {
    encrypt: false,
    trustServerCertificate: true
  }
};

async function ensureDatabase() {
  try {
    const masterConfig = Object.assign({}, dbConfig, { database: 'master' });
    const pool = await sql.connect(masterConfig);
    const check = await pool.request().query(`SELECT db_id('${dbConfig.database}') AS dbid`);
    if (!check.recordset || !check.recordset[0].dbid) {
      console.log(`Base de datos ${dbConfig.database} no existe. Creando...`);
      await pool.request().query(`CREATE DATABASE [${dbConfig.database}]`);
      console.log('Base de datos creada.');
    }
    await pool.close();
  } catch (err) {
    console.error('Error al asegurar la base de datos:', err);
    throw err;
  }
}

async function initSchemaIfNeeded() {
  try {
    const pool = await sql.connect(dbConfig);
    const exists = await pool.request().query("SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME='Proyecto'");
    if (!exists.recordset || exists.recordset.length === 0) {
      const initPath = process.env.SQL_INIT_PATH || path.join(__dirname, 'init.sql');
      if (fs.existsSync(initPath)) {
        const script = fs.readFileSync(initPath, 'utf8');
        console.log('Inicializando esquema desde', initPath);
        // Split by GO statements if present
        const parts = script.split(/^GO\s*$/im).map(s => s.trim()).filter(Boolean);
        for (const part of parts) {
          await pool.request().batch(part);
        }
        console.log('Esquema inicializado.');
      } else {
        console.warn('No se encontró init.sql en backend; no se inicializó esquema.');
      }
    }
    await pool.close();
  } catch (err) {
    console.error('Error inicializando esquema:', err);
    throw err;
  }
}

async function startServer() {
  try {
    await ensureDatabase();
    await initSchemaIfNeeded();
  } catch (err) {
    console.warn('No se pudo inicializar DB automáticamente; se seguirá con datos estáticos.', err.message);
  }

  app.get('/api/materiales', async (req, res) => {
    try {
      const pool = await sql.connect(dbConfig);
      const result = await pool.request().query('SELECT id_material AS id, nombre, descripcion, cantidad, uso FROM Materiales');
      await pool.close();
      return res.json(result.recordset || STATIC_MATERIALES);
    } catch (err) {
      console.error('Error consultando Materiales:', err.message);
      return res.json(STATIC_MATERIALES);
    }
  });

  app.post('/api/comentarios', async (req, res) => {
    const { nombre, email, sensacion, comentario } = req.body;
    if (!nombre || !email || !sensacion || !comentario) {
      return res.status(400).json({ error: 'Faltan datos obligatorios.' });
    }
    // Simple persist to in-memory list for now
    // Could be extended to insert into DB
    const nuevoComentario = { id: Date.now(), nombre, email, sensacion, comentario, fecha: new Date().toISOString() };
    // respond created
    res.status(201).json(nuevoComentario);
  });

  app.get('/api/comentarios', (req, res) => {
    res.json([]);
  });

  app.listen(port, () => {
    console.log(`Backend iniciado en http://localhost:${port}`);
  });
}

startServer();
