document.getElementById("registerForm")
.addEventListener("submit", async function(e){

    e.preventDefault();

    const payload = {
        full_name: document.getElementById("full_name").value,
        email: document.getElementById("email").value,
        phone: document.getElementById("phone").value,
        college_company: document.getElementById("college_company").value,
        stream: document.getElementById("stream").value,
        experience: document.getElementById("experience").value
    };

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/candidate/register",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            }
        );

        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }

        const result = await response.json();

        alert("Registration Successful!");

        localStorage.setItem(
            "candidate_id",
            result.candidate_id
        );

        window.location.href = "/exam";

    }
    catch(error){
        console.error(error);
        alert("Registration failed. Check backend server and console.");
    }
});