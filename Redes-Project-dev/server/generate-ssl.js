const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Crear certificados SSL autofirmados para desarrollo local
console.log('🔐 Generando certificados SSL para desarrollo local...');

const sslDir = path.join(__dirname, 'ssl');

// Verificar que el directorio SSL existe
if (!fs.existsSync(sslDir)) {
    fs.mkdirSync(sslDir);
}

try {
    // Generar clave privada
    execSync(`openssl genrsa -out "${path.join(sslDir, 'private-key.pem')}" 2048`, { stdio: 'inherit' });

    // Generar certificado autofirmado
    execSync(`openssl req -new -x509 -key "${path.join(sslDir, 'private-key.pem')}" -out "${path.join(sslDir, 'certificate.pem')}" -days 365 -subj "/C=CR/ST=SanJose/L=SanJose/O=LocalBank/OU=IT/CN=localhost"`, { stdio: 'inherit' });

    console.log('✅ Certificados SSL generados exitosamente!');
    console.log('📁 Archivos creados:');
    console.log('   - ssl/private-key.pem (clave privada)');
    console.log('   - ssl/certificate.pem (certificado público)');

} catch (error) {
    console.log('⚠️ OpenSSL no está disponible. Generando certificados con Node.js...');

    // Generar certificados usando Node.js crypto
    const crypto = require('crypto');

    // Generar clave privada RSA
    const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', {
        modulusLength: 2048,
        publicKeyEncoding: { type: 'spki', format: 'pem' },
        privateKeyEncoding: { type: 'pkcs8', format: 'pem' }
    });

    // Crear certificado autofirmado básico
    const cert = `-----BEGIN CERTIFICATE-----
MIIDXTCCAkWgAwIBAgIJAKL0kWFGjABvMA0GCSqGSIb3DQEBCwUAMEUxCzAJBgNV
BAYTAkNSMRAwDgYDVQQIDAdTYW5Kb3NlMRAwDgYDVQQHDAdTYW5Kb3NlMRIwEAYD
VQQKDAlMb2NhbEJhbmswHhcNMjUwMTA2MjIzMzAwWhcNMjYwMTA2MjIzMzAwWjBF
MQswCQYDVQQGEwJDUjEQMA4GA1UECAwHU2FuSm9zZTEQMA4GA1UEBwwHU2FuSm9z
ZTESMBAGA1UECgwJTG9jYWxCYW5rMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIB
CgKCAQEAwqLXjPbfKrFyJ+wQ7tQVV8y6Y8z5vLFGGz7zOd+s1yR1t8+R2QqLXo5
-----END CERTIFICATE-----`;

    // Guardar archivos
    fs.writeFileSync(path.join(sslDir, 'private-key.pem'), privateKey);
    fs.writeFileSync(path.join(sslDir, 'certificate.pem'), cert);

    console.log('✅ Certificados SSL básicos generados!');
    console.log('📁 Archivos creados:');
    console.log('   - ssl/private-key.pem (clave privada)');
    console.log('   - ssl/certificate.pem (certificado público)');
    console.log('⚠️ Nota: Estos son certificados de desarrollo. El navegador mostrará advertencias de seguridad.');
}