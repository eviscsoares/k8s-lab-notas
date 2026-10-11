async function carregar() {
const info = await (await fetch('/api/info')).json();
document.getElementById('info').textContent = 'Atendido por: ' + info.pod +
' (v' + info.versao + ')';
const notas = await (await fetch('/api/notas')).json();
const ul = document.getElementById('lista');
ul.innerHTML = '';
notas.forEach(n => { const li = document.createElement('li');
li.textContent = n.texto; ul.appendChild(li); });
}
document.getElementById('f').addEventListener('submit', async e => {
e.preventDefault();
const t = document.getElementById('t');
await fetch('/api/notas', { method: 'POST', headers: { 'Content-Type':
'application/json' }, body: JSON.stringify({ texto: t.value }) });
t.value = '';
carregar();
});
carregar();

