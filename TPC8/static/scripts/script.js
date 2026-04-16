function apagar_conceito(designacao){
    $.ajax("/conceitos/" + designacao, {
        method: "DELETE",       //caso haja um pedido
        success: function(response){        //se for bem sucedido, faz isto:
            alert("Correu bem!")
            window.location.href = "/conceitos"
        },
        error: function(response){      //se der erro/for mal sucedido, faz isto:
            alert("Correu mal!")
            console.log(response)
        }
    })
}

new DataTable('#tabela_conceitos')