import "./styles.css";

// FASE 0: solo la prova che lo stack gira. La macchina a stati del timer arriverà
// in FASE 2 e vivrà in src/timer/ (logica pura, testabile senza DOM).
const app = document.querySelector<HTMLDivElement>("#app");
if (!app) throw new Error("#app non trovato in index.html");

app.innerHTML = `
  <div class="placeholder">
    <h1>Ripeti</h1>
    <p>Scheletro del progetto pronto — versione 0.1.0</p>
  </div>
`;
