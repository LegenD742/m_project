document.getElementById("analyzeBtn").addEventListener("click", async () => {
  const code = document.getElementById("codeInput").value;
  if (!code.trim()) {
    alert("Please enter some code first!");
    return;
  }

  // Collect selected clone types
  const selected = [];
  document.querySelectorAll('input[type="checkbox"]:checked').forEach(cb => {
    const label = cb.nextElementSibling.textContent.toLowerCase();
    if (label.includes("type-1")) selected.push("type1");
    if (label.includes("type-2")) selected.push("type2");
    if (label.includes("type-3")) selected.push("type3");
  });

  // disable button
  const analyzeBtn = document.getElementById("analyzeBtn");
  analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Analyzing...';
  analyzeBtn.disabled = true;

  try {
    const response = await fetch("/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        code: code,
        compare_code: code, // later replaced by GitHub code
        clone_types: selected,
      }),
    });

    const data = await response.json();
    console.log("Response:", data);

    // Update progress bars
    document.getElementById("similarityBar").style.width = data.overall_similarity + "%";
    document.getElementById("similarityText").textContent = data.overall_similarity + "% overall similarity";

    document.getElementById("type1Bar").style.width = data.type1 + "%";
    document.getElementById("type1Percent").textContent = data.type1 + "%";

    document.getElementById("type2Bar").style.width = data.type2 + "%";
    document.getElementById("type2Percent").textContent = data.type2 + "%";

    // Reset button
    analyzeBtn.innerHTML = '<i class="fas fa-search mr-2"></i>Analyze Code for Clones';
    analyzeBtn.disabled = false;

  } catch (err) {
    console.error("Error:", err);
    alert("Error analyzing code");
    analyzeBtn.innerHTML = '<i class="fas fa-search mr-2"></i>Analyze Code for Clones';
    analyzeBtn.disabled = false;
  }
});
