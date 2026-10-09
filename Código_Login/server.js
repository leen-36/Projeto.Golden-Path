const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
const port = 3000;

app.use(express.json());
app.use(express.static(__dirname)); // Mantém seus arquivos HTML/CSS acessíveis

app.post('/login', (req, res) => {
    try {
        const { user, senha, tipo } = req.body;

        // 1. TESTE PRIORITÁRIO (Dados fixos que você pediu)
        if (tipo === "PROFESSOR" && user === "56490021854" && senha === "Chef") {
            return res.json({
                success: true,
                nome: "Mestra Professora",
                turma: "painel_professor", // O frontend vai completar com .html
                redirect: "painel_professor.html"
            });
        }

        // 2. LOGICA ORIGINAL (Busca no usuarios.json)
        if (fs.existsSync('usuarios.json')) {
            const usuarios = JSON.parse(fs.readFileSync('usuarios.json', 'utf8'));
            
            // Limpa o RA ou CPF (remove pontos, traços e espaços)
            const documentoLimpo = user.replace(/[^0-9xX]/g, "");
            
          // Busca no arquivo fazendo a limpeza do campo 'u.user' também!
          const conta = usuarios.find(u => {
            // Remove pontos e traços do documento que está salvo no JSON antes de comparar
            const userJsonLimpo = u.user.replace(/[^0-9xX]/g, "");
            return userJsonLimpo === documentoLimpo && u.senha === senha;
        });

            if (conta) {
                let destino = "";
                // Identifica se é professor ou aluno no JSON
                if (conta.tipo.toLowerCase() === "professor") {
                    destino = "painel_professor";
                } else {
                    destino = conta.turma;
                }

                return res.json({ 
                    success: true, 
                    nome: conta.nome,
                    turma: destino, // Para compatibilidade com seu código antigo
                    redirect: destino + ".html"
                });
            }
        }

        // 3. SE CHEGAR AQUI, FALHOU
        res.json({ success: false, message: "RA/CPF ou Senha Incorretos!" });

    } catch (error) {
        console.error("Erro interno:", error);
        res.status(500).json({ success: false, message: "Erro no servidor ao processar login." });
    }
});

// Inicia o servidor uma única vez (A tomada que liga o sistema!)
app.listen(port, () => {
    console.log(`
    ----------------------------------------------
    Motor Golden Path ativo!
    Acesse: http://localhost:${port}
    ----------------------------------------------
    `);
});
