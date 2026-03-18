async function analyze() {
    const deps = document.getElementById("deps").value;

    const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ dependencies: deps.split("\n") })
    });

    const data = await response.json();
    document.getElementById("result").innerText = JSON.stringify(data, null, 2);
}