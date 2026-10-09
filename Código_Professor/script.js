
// ==========================================
// SALA DO FUTURO — DADOS DEMONSTRATIVOS
// ==========================================

const aluno = {

    nome: "Leen",

    turma: "3º Ano — Técnico",

    matricula: "2025001",

    presenca: 92,

    tarefas: 4,

    notificacoes: 3,

    media: 8.5

};


// ==========================================
// ATUALIZAR PAINEL
// ==========================================

function atualizarPainel() {

    document.getElementById("user-name").textContent =
        aluno.nome;

    document.getElementById("user-class").textContent =
        aluno.turma;

    document.getElementById("user-registration").textContent =
        aluno.matricula;

    document.getElementById("attendance").textContent =
        aluno.presenca + "%";

    document.getElementById("attendance-bar").style.width =
        aluno.presenca + "%";

    document.getElementById("tasks").textContent =
        aluno.tarefas;

    document.getElementById("notifications").textContent =
        aluno.notificacoes;

    document.getElementById("average").textContent =
        aluno.media.toFixed(1);

}


// ==========================================
// MENU LATERAL
// ==========================================

const menuItems = document.querySelectorAll(".menu-item");

const updateMessage = document.getElementById("update-message");

menuItems.forEach(item => {

    item.addEventListener("click", () => {

        menuItems.forEach(button => {

            button.classList.remove("active");

        });

        item.classList.add("active");

        const section = item.dataset.section;

        const messages = {

            painel: "Painel demonstrativo",

            tarefas: "Tarefas pendentes: " + aluno.tarefas,

            notificacoes:
                "Notificações não lidas: " + aluno.notificacoes,

            boletim:
                "Média geral: " + aluno.media.toFixed(1),

            presenca:
                "Frequência escolar: " + aluno.presenca + "%"

        };

        updateMessage.textContent =
            messages[section] || "Painel demonstrativo";

    });

});


// ==========================================
// DATA DE ATUALIZAÇÃO
// ==========================================

function mostrarData() {

    const agora = new Date();

    const data = agora.toLocaleDateString("pt-BR", {

        day: "2-digit",

        month: "2-digit",

        year: "numeric"

    });

    document.getElementById("date").textContent =
        "ATUALIZADO EM " + data;

}


// ==========================================
// INICIAR
// ==========================================

atualizarPainel();

mostrarData();