document.addEventListener('DOMContentLoaded', () => {
    // LOGIN
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', (event) => {
            const emailLogin = document.getElementById('emailLogin').value.trim();
            const senhaLogin = document.getElementById('senhaLogin').value.trim();

            if (!emailLogin || !senhaLogin) {
                event.preventDefault();
                alert('Por favor, preencha todos os campos.');
            }
            // Se ok, deixa enviar normalmente
        });
    }

    // CADASTRO
    const cadastroForm = document.getElementById('cadastroForm');
    if (cadastroForm) {
        cadastroForm.addEventListener('submit', (event) => {
            const nome = document.getElementById('nomeCadastro').value.trim();
            const email = document.getElementById('emailCadastro').value.trim();
            const senha = document.getElementById('senhaCadastro').value;
            const confirmar = document.getElementById('confirmarSenhaCadastro').value;

            if (!nome || !email || !senha || !confirmar) {
                event.preventDefault();
                alert('Preencha todos os campos.');
                return;
            }

            if (senha !== confirmar) {
                event.preventDefault();
                alert('As senhas não coincidem!');
                return;
            }
            // Se ok, deixa enviar normalmente para o Flask
        });
    }

    // LOGOUT
    const logoutButton = document.getElementById('logoutButton');
    if (logoutButton) {
        logoutButton.addEventListener('click', () => {
            window.location.href = '/logout';
        });
    }
});