document.addEventListener("DOMContentLoaded", function () {

 /* ================= PASSWORD ANALYZER ================= */

const passwordForm = document.getElementById("passwordForm");
const passwordInput = document.getElementById("passwordInput");
const strengthBar = document.getElementById("strengthBar");

if (passwordForm && passwordInput) {

    passwordForm.addEventListener("submit", async function (e) {

        e.preventDefault();

        const password = passwordInput.value;

        try {

            const res = await fetch("/analyze_password", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ password })
            });

            const data = await res.json();

            // Reveal the results container
            document.getElementById("passwordResults").style.display = "block";

            const bar = document.getElementById("strengthBar");

            let color = "#2ecc71";
            let width = "90%";

            if (data.strength === "Very Weak") {
                color = "#e74c3c";
                width = "20%";
            }
            else if (data.strength === "Weak") {
                color = "#ff6b6b";
                width = "40%";
            }
            else if (data.strength === "Medium") {
                color = "#f1c40f";
                width = "60%";
            }
            else if (data.strength === "Strong") {
                color = "#2ecc71";
                width = "85%";
            }

            bar.style.background = color;
            bar.style.width = width;
            bar.style.boxShadow = `0 0 10px ${color}`;

            document.getElementById("strengthText").innerText = data.strength;
            document.getElementById("lengthText").innerText = data.length;
            document.getElementById("complexityText").innerText = data.complexity;
            document.getElementById("dictionaryText").innerText = data.dictionary;
            document.getElementById("crackText").innerText = data.time;

        } catch (error) {
            console.error("Password analysis error:", error);
        }

    });
}

    /* ================= EMAIL BREACH CHECK ================= */

    const emailForm = document.getElementById("emailForm");

    if (emailForm) {

        emailForm.addEventListener("submit", async function (e) {

            e.preventDefault();

            const emailInputEl = document.getElementById("emailInput");
            if (!emailInputEl) return;
            
            const email = emailInputEl.value;
            const box = document.getElementById("emailResult");

            try {

                const res = await fetch("/check_email", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ email: email })
                });

                const data = await res.json();

                if (!box) return;

                if (data.breached) {

                    box.innerHTML = `
                    <div class="result-card danger fade-in">
                        <div class="risk-badge high">HIGH RISK</div>

                        <h3>⚠ Email Found in Breach</h3>

                        <div class="info-grid">
                            <div><strong>Breach Name:</strong> ${data.breach}</div>
                            <div><strong>Year:</strong> ${data.year}</div>
                            <div><strong>Exposed Data:</strong> ${data.data}</div>
                            <div><strong>Risk Score:</strong> ${data.risk_score}%</div>
                        </div>

                        <hr>

                        <p><strong>SHA1 Hash:</strong><br>${data.email_hash}</p>
                        <p><small>Checked at: ${data.checked_at}</small></p>

                        <div class="recommendation">
                            🔐 ${data.recommendation}
                        </div>
                    </div>
                    `;

                } else {

                    box.innerHTML = `
                    <div class="result-card safe fade-in">

                        <div class="risk-badge low">LOW RISK</div>

                        <h3>✔ No Breach Found</h3>

                        <p>This email is not found in the breach database.</p>

                        <p><strong>Risk Score:</strong> ${data.risk_score}%</p>
                        <p><strong>SHA1 Hash:</strong><br>${data.email_hash}</p>
                        <p><small>Checked at: ${data.checked_at}</small></p>

                        <div class="recommendation safe-rec">
                            🛡 ${data.recommendation}
                        </div>

                    </div>
                    `;
                }

            } catch (error) {

                if (box) {
                    box.innerHTML = "<p style='color:red;'>Error checking email.</p>";
                }

                console.error("Email check error:", error);
            }

        });

    }


    // ================= PHISHING DETECTION =================

    const phishingForm = document.getElementById("phishingForm");

    if (phishingForm) {

        phishingForm.addEventListener("submit", async function (e) {

            e.preventDefault();

            const phishingInputEl = document.getElementById("phishingInput");
            if (!phishingInputEl) return;
            
            const content = phishingInputEl.value;
            const box = document.getElementById("phishingResult");

            if (!content.trim()) return;

            // Loading animation
            box.innerHTML = `
            <div class="result-card">
                <p>🔍 Analyzing message...</p>
            </div>
            `;

            try {

                const res = await fetch("/detect_phishing", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ content: content })
                });

                const data = await res.json();

                let riskClass = "low-risk";

                if (data.risk_level === "HIGH RISK") riskClass = "high-risk";
                else if (data.risk_level === "MEDIUM RISK") riskClass = "medium-risk";

                box.innerHTML = `
                <div class="result-card ${riskClass}">

                    <h3>${data.risk_level}</h3>

                    <p><strong>Risk Score:</strong> ${data.risk_score}</p>

                    <p><strong>Risk Percentage:</strong> ${data.risk_percent}%</p>

                    <p><strong>URLs Found:</strong> 
                    ${data.urls_found.length ? data.urls_found.join(", ") : "None"}
                    </p>

                    <ul>
                    ${data.reasons.map(r => `<li>${r}</li>`).join("")}
                    </ul>

                </div>
                `;

            } catch (error) {

                box.innerHTML = `
                <div class="result-card high-risk">
                    <p>❌ Error analyzing content.</p>
                </div>
                `;

                console.error("Phishing detection error:", error);
            }

        });

    }

});
