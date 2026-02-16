from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse

app = FastAPI(title="Gerenciador de Tarefas")

tarefas: list[dict] = []

class TarefaCreate(BaseModel):
    nome: str = Field(min_length=1)
    descricao: str = Field(min_length=1)

@app.post("/tarefas", status_code=201)
def adicionar_tarefa(tarefa: TarefaCreate):

    if any(t["nome"] == tarefa.nome for t in tarefas):
        raise HTTPException(status_code=409, detail="Já existe uma tarefa com esse nome.")

    nova = {"nome": tarefa.nome, "descricao": tarefa.descricao, "concluida": False}
    tarefas.append(nova)
    return JSONResponse(
    status_code=201,
    content={"mensagem": "Tarefa adicionada com sucesso.", "tarefa": nova},
)

@app.get("/tarefas")
def listar_tarefas():
    return tarefas

@app.put("/tarefas/{nome}")
def concluir_tarefa(nome: str):
    for t in tarefas:
        if t["nome"] == nome:
            t["concluida"] = True
            return t
    raise HTTPException(status_code=404, detail="Tarefa não encontrada.")

@app.delete("/tarefas/{nome}")
def remover_tarefa(nome: str):
    for i, t in enumerate(tarefas):
        if t["nome"] == nome:
            removida = tarefas.pop(i)
            return {"mensagem": "Tarefa removida com sucesso.", "tarefa": removida}
    raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
