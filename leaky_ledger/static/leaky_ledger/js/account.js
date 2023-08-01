var creditScore = 780;

$(function () {
  $("#destinationEmail").autocomplete({
    source: function (request, response) {
      $.ajax({
        url: "/users/lookup/",
        data: { term: request.term },
        success: function (data) {
          response(data.map(u => u.email));
        },
      });
    },
    minLength: 1,
  });
});

$("#externalTransferCheck").change(function () {
  if (this.checked) {
    $("#internalTransfer").hide();
    $("#externalTransfer").show();
  } else {
    $("#internalTransfer").show();
    $("#externalTransfer").hide();
  }
});

function checkForm() {
  let source = $("#sourceAccount").val();
  let destination = $("#externalTransferCheck").is(":checked")
    ? $("#destinationEmail").val()
    : $("#destinationAccount").val();
  let amount = $("#transferAmount").val();

  if (source && destination && amount) {
    $("#confirmTransfer").prop("disabled", false);
  } else {
    $("#confirmTransfer").prop("disabled", true);
  }
}

function decreaseCreditScore() {
  var decreaseAmount = Math.floor(Math.random() * 10) + 1;
  creditScore -= decreaseAmount;

  if (creditScore < 0) {
    creditScore = 0;
  }

  document.getElementById("credit-score").textContent = creditScore;
}

setInterval(decreaseCreditScore, 10000);

$(
  "#sourceAccount, #destinationAccount, #destinationEmail, #transferAmount, #externalTransferCheck"
).change(checkForm);

checkForm();
