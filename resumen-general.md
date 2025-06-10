# Análisis: Redes-Project-dev/server (Banco TypeScript)

## 🏦 Resumen General

Banco implementado en TypeScript/Node.js con Prisma ORM. Representa otro banco participante en el ecosistema SINPE, con arquitectura más robusta y completa.

## 🔄 Estado de Conectividad con Banco Python

- ✅ **Recepción desde Python**: Endpoints compatibles
- ⚠️ **Envío hacia Python**: Requiere HMAC corregido en banco Python
- ✅ **Protocolo SINPE**: Estructura de payloads estándar
- ✅ **SSL/TLS**: Comunicación segura implementada

## 📁 Estructura del Proyecto

```txt
server/
├── src/
│   ├── index.ts              # Punto de entrada
│   ├── config/               # Configuraciones
│   ├── controller/           # Controladores
│   ├── model/                # Modelos de datos
│   ├── prisma/               # Configuración Prisma
│   └── routes/               # Rutas de API
├── prisma/
│   ├── bccr/                 # Esquemas BCCR
│   ├── generated/            # Código generado
│   └── sinpe/                # Esquemas SINPE
├── ssl/                      # Certificados SSL
├── package.json              # Dependencias Node.js
└── tsconfig.json             # Configuración TypeScript
```

## 🔧 Stack Tecnológico

### Backend Framework

- **TypeScript**: Lenguaje principal
- **Node.js**: Runtime
- **Express.js**: Framework web
- **Prisma**: ORM para base de datos

### Base de Datos

- **Prisma Schema**: Definición de modelos
- **Migraciones**: Control de versiones de BD
- **Generación de tipos**: Type safety automático

## 📡 Arquitectura de API

### Controladores Principales

```typescript
// Controlador SINPE
export class SinpeController {
    async receiveSinpeTransfer(req: Request, res: Response)
    async receiveSinpeMovilTransfer(req: Request, res: Response) 
    async validatePhone(req: Request, res: Response)
    async getBankInfo(req: Request, res: Response)
}
```

### Rutas de API

```txt
POST /api/sinpe/transfer          # Transferencias SINPE
POST /api/sinpe/movil            # SINPE móvil
GET  /api/sinpe/validate/:phone  # Validación teléfono
GET  /api/bank/info              # Información del banco
GET  /health                     # Health check
```

## 🔐 Seguridad Avanzada

### SSL/TLS

- Certificados SSL configurados
- Comunicación HTTPS entre bancos
- Validación de certificados

### Autenticación Multi-layer

```typescript
// Middleware de autenticación
const authenticateBank = (req: Request, res: Response, next: NextFunction) => {
    // Verificar certificado SSL
    // Validar HMAC signature
    // Verificar banco autorizado
    next();
}
```

### Validación de Payload

```typescript
interface SinpeTransferPayload {
    version: string;
    timestamp: string;
    transaction_id: string;
    sender: BankAccount;
    receiver: BankAccount;
    amount: Amount;
    description: string;
    hmac_md5: string;
}
```

## 🗄️ Modelo de Datos (Prisma)

### Esquemas Principales

```prisma
model User {
    id        String   @id @default(cuid())
    name      String
    email     String   @unique
    phone     String?
    accounts  Account[]
    createdAt DateTime @default(now())
}

model Account {
    id           String        @id @default(cuid()) 
    number       String        @unique
    balance      Decimal
    currency     String        @default("CRC")
    userId       String
    user         User          @relation(fields: [userId], references: [id])
    transactions Transaction[]
}

model Transaction {
    id            String   @id @default(cuid())
    transactionId String   @unique
    fromAccountId String?
    toAccountId   String
    amount        Decimal
    currency      String   @default("CRC")
    status        String   @default("pending")
    type          String   # sinpe, sinpe_movil, internal
    externalBank  String?
    createdAt     DateTime @default(now())
}
```

## 🔄 Flujo de Procesamiento Avanzado

### Pipeline de Transferencias

1. **Validación de Entrada**
   - Schema validation con Joi/Zod
   - Verificación de tipos TypeScript
   - Sanitización de datos

2. **Autenticación**
   - Verificar certificado SSL del banco sender
   - Validar HMAC signature
   - Confirmar banco en whitelist

3. **Procesamiento de Negocio**
   - Verificar cuenta destino existe
   - Validar límites de transferencia
   - Aplicar reglas de negocio específicas

4. **Transacción de Base de Datos**

   ```typescript
   await prisma.$transaction(async (tx) => {
       // Acreditar cuenta destino
       await tx.account.update({
           where: { number: receiverAccount },
           data: { balance: { increment: amount } }
       });
       
       // Crear registro de transacción
       await tx.transaction.create({
           data: transactionData
       });
   });
   ```

5. **Respuesta y Logging**
   - Log completo de la operación
   - Respuesta estructurada al banco sender
   - Notificaciones si aplican

## 🌐 Comunicación Inter-banco

### Cliente HTTP para Bancos Externos

```typescript
class BankConnector {
    async sendSinpeTransfer(targetBank: string, payload: SinpePayload) {
        const bankConfig = this.getBankConfig(targetBank);
        
        const response = await axios.post(
            `${bankConfig.url}/api/sinpe/transfer`,
            payload,
            {
                httpsAgent: new https.Agent({
                    cert: this.getClientCert(),
                    key: this.getClientKey()
                })
            }
        );
        
        return response.data;
    }
}
```

### Configuración de Bancos

```typescript
interface BankConfig {
    code: string;
    name: string;
    url: string;
    certificate: string;
    publicKey: string;
    enabled: boolean;
}
```

## 🧪 Sistema de Pruebas

### Testing Framework

- **Jest**: Framework de testing
- **Supertest**: Testing de APIs
- **Prisma Test Environment**: BD de pruebas

### Casos de Prueba

```typescript
describe('SINPE Transfer', () => {
    test('should process valid transfer', async () => {
        const payload = createValidPayload();
        const response = await request(app)
            .post('/api/sinpe/transfer')
            .send(payload)
            .expect(200);
            
        expect(response.body.success).toBe(true);
    });
});
```

## ⚙️ Configuración y Deployment

### Variables de Entorno

```env
DATABASE_URL="postgresql://..."
BANK_CODE="119"
BANK_NAME="Banco TypeScript"
SSL_CERT_PATH="./ssl/cert.pem"
SSL_KEY_PATH="./ssl/key.pem"
HMAC_SECRET="supersecreta123"
```

### Scripts de Deployment

```json
{
    "scripts": {
        "build": "tsc",
        "start": "node dist/index.js", 
        "dev": "ts-node-dev src/index.ts",
        "migrate": "prisma migrate deploy",
        "generate": "prisma generate"
    }
}
```

## 🔧 Integración con Ecosistema SINPE

- **Protocolo Compatible**: Misma estructura de payloads que banco Python
- **HMAC Verification**: Algoritmo idéntico para validación
- **Error Handling**: Códigos de respuesta estándar
- **Logging**: Formato consistente para auditoría
- **Health Monitoring**: Endpoints de monitoreo para disponibilidad
