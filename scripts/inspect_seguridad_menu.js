
const axios = require('axios');

async function checkMenu() {
    try {
        // Authenticate first (simulate logic or just use known token if persisted, but better to login)
        // For simplicity in this environment, I'll assume I can just hit the local API if I have a token or mock it.
        // Actually, I need to login to get a token.

        const loginRes = await axios.post('http://localhost:8000/api/v1/auth/login', {
            usuario_email: 'admin@facturacion.com',
            usuario_password: 'admin'
        }, {
            headers: { 'Content-Type': 'application/json' }
        });

        // Extract cookies
        const cookies = loginRes.headers['set-cookie'];
        console.log('Cookies obtained:', cookies);

        const menuRes = await axios.get('http://localhost:8000/api/v1/usuarios/me/menu', {
            headers: {
                'Cookie': cookies.join('; ') // Send back cookies
            }
        });

        const items = menuRes.data;
        // Filter for relevant items
        const seguridad = items.find(i => i.nombre.includes('Seguridad'));
        const usuarios = items.find(i => i.nombre.includes('Usuari'));
        const roles = items.find(i => i.nombre.includes('Rol'));
        const menus = items.find(i => i.nombre === 'Menús' || i.nombre === 'Menus' || i.nombre.includes('Menu'));

        console.log('--- Seguridad Item ---');
        console.log(seguridad || 'NOT FOUND');

        console.log('--- Children Items ---');
        const parent4 = items.find(i => i.id === 4);
        console.log('--- Parent ID 4 ---');
        console.log(parent4 || 'NOT FOUND');
    } catch (e) {
        console.error('Error:', e.message);
        if (e.response) console.error('Response:', e.response.data);
    }
}

checkMenu();
