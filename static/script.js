document.getElementById("analyzeForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const url = document.getElementById("url").value;
    const result = document.getElementById("result");

    result.innerHTML = "<p>Analyzing...</p>";

    try {
        const response = await fetch("/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                url: url
            })
        });

        const data = await response.json();

        if (!response.ok) {
            result.innerHTML = '<p style="color:red;">${data.error}</p>';
            return;
        }

        result.innerHTML = `
            <div class="report">
                <div class="card"><b>HTTP Status:</b> ${data.status}</div>
                <div class="card"><b>Response Time:</b> ${data.response_time} sec</div>
                <div class="card"><b>Title:</b> ${data.title}</div>
                <div class="card"><b>Meta Description:</b> ${data.meta}</div>
                <div class="card"><b>H1 Count:</b> ${data.h1}</div>
                <div class="card"><b>Images Missing Alt:</b> ${data.missing_alt}</div>
                <div class="card"><b>Word Count:</b> ${data.word_count}</div>
            </div>
        `;
    } catch (error) {
        result.innerHTML = '<p style="color:red;">Error: ${error.message}</p>';
    }
});