
const aluno = {
    nome: "Leen_mistica",
    turma: "3º Ano — Técnico",
    matricula: "2025001",
    presenca: 92,
    tarefasPendentes: 6,
    notificacoes: 126,
    mediaGeral: 9.0
  };
  
  // Dados fictícios para o protótipo.
  // Depois, substituiremos este objeto pela integração com o servidor.
  let petAlimentado = false;
  
  const $ = (id) => document.getElementById(id);
  
  const botaoDados = $("verDados");
  const botaoAlimentar = $("alimentarPet");
  const painelDados = $("painelDados");
  const esquilo = $("esquilo");
  const mensagem = $("mensagem");
  const efeitoNozes = $("efeitoNozes");
  
  function carregarDados() {
    $("nomeTopo").textContent = aluno.nome;
    $("turmaTopo").textContent = aluno.turma;
  
    $("nomeAluno").textContent = aluno.nome;
    $("turmaAluno").textContent = aluno.turma;
    $("matriculaAluno").textContent = aluno.matricula;
  
    $("presencaValor").textContent = `${aluno.presenca}%`;
    $("barraPresenca").style.width =
      `${Math.max(0, Math.min(100, aluno.presenca))}%`;
  
    $("tarefasValor").textContent = aluno.tarefasPendentes;
    $("notificacoesValor").textContent = aluno.notificacoes;
    $("mediaValor").textContent = aluno.mediaGeral.toLocaleString("pt-BR", {
      minimumFractionDigits: 1,
      maximumFractionDigits: 1
    });
  
    atualizarBotaoAlimentar();
  }
  
  function atualizarBotaoAlimentar() {
    const temPendencias = aluno.tarefasPendentes > 0;
  
    botaoAlimentar.disabled = temPendencias || petAlimentado;
  
    if (temPendencias) {
      $("textoAlimentar").textContent = "Conclua suas atividades primeiro";
      botaoAlimentar.title =
        "Conclua as atividades pendentes para alimentar o pet.";
    } else if (petAlimentado) {
      $("textoAlimentar").textContent = "Pet alimentado nesta visita";
      botaoAlimentar.title = "Você já alimentou o esquilo nesta visita.";
    } else {
      $("textoAlimentar").textContent = "Oferecer uma noz ao esquilo";
      botaoAlimentar.title = "Alimente seu companheiro uma vez.";
    }
  }
  
  function abrirDados() {
    painelDados.hidden = false;
    mensagem.textContent = "";
    $("fecharDados").focus();
  }
  
  function fecharDados() {
    painelDados.hidden = true;
    botaoDados.focus();
  }
  
  function alimentarPet() {
    if (aluno.tarefasPendentes > 0) {
      mensagem.textContent =
        `Você possui ${aluno.tarefasPendentes} atividades pendentes. ` +
        "Conclua-as primeiro! Você pode visualizar seus dados acima.";
      return;
    }
  
    if (petAlimentado) {
      mensagem.textContent = "O esquilo já recebeu sua noz nesta visita!";
      return;
    }
  
    petAlimentado = true;
    atualizarBotaoAlimentar();
  
    mensagem.textContent = "O esquilo encontrou uma noz e está comendo!";
  
    esquilo.classList.add("comendo");
    efeitoNozes.classList.remove("animando");
  
    // Reinicia a animação da noz.
    void efeitoNozes.offsetWidth;
    efeitoNozes.classList.add("animando");
  
    botaoDados.disabled = true;
    botaoAlimentar.disabled = true;
  
    window.setTimeout(() => {
      esquilo.classList.remove("comendo");
      efeitoNozes.classList.remove("animando");
  
      mensagem.textContent = "Nhac, nhac! Obrigado pela noz!";
  
      botaoDados.disabled = false;
      atualizarBotaoAlimentar();
    }, 2300);
  }
  
  botaoDados.addEventListener("click", abrirDados);
  botaoAlimentar.addEventListener("click", alimentarPet);
  $("fecharDados").addEventListener("click", fecharDados);
  
  painelDados.addEventListener("click", (event) => {
    if (event.target === painelDados) {
      fecharDados();
    }
  });
  
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !painelDados.hidden) {
      fecharDados();
    }
  });
  
  carregarDados();