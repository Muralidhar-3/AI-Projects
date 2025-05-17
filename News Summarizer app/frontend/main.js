async function analyzeNews() {
      const content = document.getElementById("newsInput").value;
      const response = await fetch("http://127.0.0.1:8000/analyze/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content })
      });
      const data = await response.json();
      document.getElementById("summary").textContent = data.summary;
      document.getElementById("sentiment").textContent = `${data.sentiment.label} (${data.sentiment.score.toFixed(2)})`;
    }