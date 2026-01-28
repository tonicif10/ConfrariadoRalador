
document.addEventListener("DOMContentLoaded", function () {
    if (!localStorage.getItem("cookiesAccepted")) {
        const cookieBanner = document.createElement("div");
        cookieBanner.id = "cookie-banner";
        cookieBanner.innerHTML = `
            <div style="position: fixed; bottom: 20px; left: 20px; right: 20px; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); z-index: 9999; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 15px; border-left: 5px solid #722F37;">
                <p style="margin: 0; font-family: 'Lato', sans-serif; color: #333; font-size: 14px; line-height: 1.5;">
                    Utilizamos cookies para melhorar a sua experiência no site da <strong>Confraria do Ralador</strong>. Ao continuar a navegar, aceita a nossa utilização de cookies.
                </p>
                <button id="accept-cookies" style="background: #722F37; color: #D4AF37; border: none; padding: 10px 20px; border-radius: 4px; font-family: 'Playfair Display', serif; font-weight: bold; cursor: pointer; transition: all 0.3s ease;">
                    Aceitar
                </button>
            </div>
        `;
        document.body.appendChild(cookieBanner);

        document.getElementById("accept-cookies").addEventListener("click", function () {
            localStorage.setItem("cookiesAccepted", "true");
            cookieBanner.style.opacity = "0";
            setTimeout(() => cookieBanner.remove(), 300);
        });
    }
});
