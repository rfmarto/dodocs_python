$(document).ready(function() {

  function limpa_formulário_cnpj() {
      // Limpa valores do formulário de CNPJ.
      $("nome").val("");
      $("fantasia").val("");
      $("cnpj").val("");
      $("email").val("");
      $("telefone").val("");
      $("atualizacao").val("");
      $("abertura").val("");
      $("atividade_principal").val("");
      $("code").val("");
  
      $("#rua").val("");
      $("#bairro").val("");
      $("#municipio").val("");
      $("#uf").val("");
      $("#ibge").val("");
  }
  
  //Quando o campo cep perde o foco.
  $("#cnpj").blur(function() {
    var cnpj = $('#cnpj').val().replace(/[^0-9]/g, '');
  
  // Fazemos uma verificação simples do cnpj confirmando se ele tem 14 caracteres
  if(cnpj.length == 14) {
  
  // Aqui rodamos o ajax para a url da API concatenando o número do CNPJ na url
  $.ajax({
  url:'https://www.receitaws.com.br/v1/cnpj/' + cnpj,
  method:'GET',
  dataType: 'jsonp', // Em requisições AJAX para outro domínio é necessário usar o formato "jsonp" que é o único aceito pelos navegadores por questão de segurança
  complete: function(xhr){
  
  // Aqui recuperamos o json retornado
  response = xhr.responseJSON;
  
  // Na documentação desta API tem esse campo status que retorna "OK" caso a consulta tenha sido efetuada com sucesso
  if(response.status == 'OK') {
  
  // Agora preenchemos os campos com os valores retornados
  $('#nome').val(response.nome);
  $('#fantasia').val(response.fantasia);
  $('#email').val(response.email);
  $('#telefone').val(response.telefone);
  $('#logradouro').val(response.logradouro);
  $('#numero').val(response.numero);
  $('#complemento').val(response.complemento);
  $("#abertura").val(response.abertura);
  $("#rua").val(response.logradouro);
  $("#bairro").val(response.bairro);
  $("#municipio").val(response.municipio);
  $("#uf").val(response.uf);
  $("#cep").val(response.cep);
  $("#atualizacao").val(response.ultima_atualizacao);
  $("#atividade_principal").val(response.atividade_principal[0].text);
  $("#code").val(response.atividade_principal[0].code);
  
  
  
  // Aqui exibimos uma mensagem caso tenha ocorrido algum erro
  } else {
  alert(response.message); // Neste caso estamos imprimindo a mensagem que a própria API retorna
  }
  }
  });
  
  // Tratativa para caso o CNPJ não tenha 14 caracteres
  } else {
  alert('CNPJ inválido');
  }
  
  });
  });