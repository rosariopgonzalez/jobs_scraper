// Función para cambiar de pestañas
function cambiarTab(tabId) {
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    
    document.getElementById(tabId).classList.add('active');
    event.target.classList.add('active');
}

// Función principal que lee el JSON y arma la página
function cargarDatos() {
    // Usamos Fetch API para leer el archivo datos.json que generó Python
    fetch('datos.json')
        .then(response => {
            if (!response.ok) {
                throw new Error("No se pudo cargar el archivo datos.json");
            }
            return response.json();
        })
        .then(empresas => {
            const tbodyBolsas = document.getElementById('tabla-bolsas');
            const tbodyLinkedin = document.getElementById('tabla-linkedin');

            // Limpiamos las tablas por si acaso
            tbodyBolsas.innerHTML = '';
            tbodyLinkedin.innerHTML = '';

            empresas.forEach(emp => {
                // Fila para la tabla de Bolsas Directas
                const filaBolsa = document.createElement('tr');
                filaBolsa.innerHTML = `
                    <td><strong>${emp.nombre}</strong></td>
                    <td><a href="${emp.web}" target="_blank">${emp.web}</a></td>
                    <td>
                        ${emp.bolsa_trabajo 
                            ? `<a href="${emp.bolsa_trabajo}" target="_blank" class="btn btn-green">✅ Ir a Empleos</a>`
                            : `<span class="btn btn-disabled">❌ No detectada</span>`}
                    </td>
                `;
                tbodyBolsas.appendChild(filaBolsa);

                // Fila para la tabla de LinkedIn
                const filaLinkedin = document.createElement('tr');
                filaLinkedin.innerHTML = `
                    <td><strong>${emp.nombre}</strong></td>
                    <td><a href="${emp.linkedin_jobs}" target="_blank" class="btn btn-blue">🔍 Revisar Empleos</a></td>
                `;
                tbodyLinkedin.appendChild(filaLinkedin);
            });
        })
        .catch(error => {
            console.error("Error al cargar los datos:", error);
            document.getElementById('tabla-bolsas').innerHTML = `<tr><td colspan="3" style="color:red; text-align:center;">Error al cargar datos.json. Revisá la consola.</td></tr>`;
        });
}

// Ejecutamos la función apenas cargue la página
cargarDatos();