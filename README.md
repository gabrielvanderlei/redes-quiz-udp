# redes-quiz-udp
Projeto de Quiz com rede UDP

## Objetivos
- Compentições online de perguntas e respostas
- Protocolo UDP próprio
- Até 5 clientes
- Ao se iniciar uma sessão novos clientes não podem entrar
- Cada competição possui 5 rodadas de perguntas e respostas
- Servidor com arquivo texto onde existem pelo menos 20 tuplas de perguntas e respostas
- Perguntas e respostas escolhidas aleatóriamente
- Uma mesma competição não pode repetir tuplas
- A rodada será encerrada quando algum participante acertar a resposta ou atingir a duração máxima de 10 segundos
- Após encerrar uma competição, um ranking de pontuação é divulgado e uma nova competição pode ser iniciada

## Pontuação
- Resposta errada: -5
- Sem resposta: -1
- Resposta correta: 25
