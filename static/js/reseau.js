document.addEventListener("DOMContentLoaded", function () {
  const deptSelect = document.getElementById("departement");
  const communeSelect = document.getElementById("commune");
  const reseauSelect = document.getElementById("reseau");
  const infosDiv = document.getElementById("infos-reseau");

  deptSelect.addEventListener("change", async function () {
    const code = this.value;
    communeSelect.innerHTML = '<option value="">-- Choisissez une commune --</option>';
    reseauSelect.innerHTML = '<option value="">-- Choisissez un réseau --</option>';
    communeSelect.disabled = true;
    reseauSelect.disabled = true;
    infosDiv.style.display = "none";

    if (!code) return;

    const res = await fetch(`/communes/${code}`);
    const communes = await res.json();

    communes.forEach(c => {
      let opt = document.createElement("option");
      opt.value = c.code;
      opt.textContent = c.nom;
      communeSelect.appendChild(opt);
    });

    communeSelect.disabled = false;
  });

  communeSelect.addEventListener("change", async function () {
    const code = this.value;
    reseauSelect.innerHTML = '<option value="">-- Choisissez un réseau --</option>';
    reseauSelect.disabled = true;
    infosDiv.style.display = "none";

    if (!code) return;

    const res = await fetch(`/reseaux/${code}`);
    const reseaux = await res.json();

    reseaux.forEach(r => {
      let opt = document.createElement("option");
      opt.value = r.code;
      opt.textContent = r.nom;
      reseauSelect.appendChild(opt);
    });

    reseauSelect.disabled = false;
  });

  reseauSelect.addEventListener("change", async function () {
    const code = this.value;
    infosDiv.style.display = "none";

    if (!code) return;

    const res = await fetch(`/infos/${code}`);
    const data = await res.json();

    document.getElementById("nom-reseau").textContent = data.nom_reseau || "";
    document.getElementById("quartier").textContent = data.quartier || "";
    document.getElementById("debut-alim").textContent = data.debut_alim || "";
    document.getElementById("annee").textContent = data.annee || "";
    document.getElementById("distributeur").textContent = data.distributeur || "";
    document.getElementById("moa").textContent = data.moa || "";

    infosDiv.style.display = "block";
  });
});
