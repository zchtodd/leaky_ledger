var creditScore = 780;

$(function () {
  $("#destinationEmail").autocomplete({
    source: function (request, response) {
      $.ajax({
        url: "/users/lookup/",
        data: { term: request.term },
        success: function (data) {
          response(data.map((u) => u.email));
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

$("#transferForm").submit(function (e) {
  e.preventDefault();

  var sourceAccount = $("#sourceAccount").val();
  var destinationAccount = $("#destinationAccount").val();
  var destinationEmail = $("#destinationEmail").val();
  var transferAmount = $("#transferAmount").val();

  var isExternalTransfer = $("#externalTransferCheck").is(":checked");
  var data;
  var url;

  if (isExternalTransfer) {
    data = {
      sourceAccount: sourceAccount,
      destinationEmail: destinationEmail,
      transferAmount: transferAmount,
    };
    url = "/transfer/external";
  } else {
    data = {
      sourceAccount: sourceAccount,
      destinationAccount: destinationAccount,
      transferAmount: transferAmount,
    };
    url = "/transfer/internal";
  }

  $.ajax({
    type: "POST",
    url: url,
    data: JSON.stringify(data),
    contentType: "application/json",
    success: function (response) {
      alert(response.message);
      $("#transferForm")[0].reset();
      $("#transferModal").modal("hide");
      location.reload();
    },
    error: function (response) {
      alert(response.responseJSON.message);
    },
  });
});

function decreaseCreditScore() {
  var decreaseAmount = Math.floor(Math.random() * 10) + 1;
  creditScore -= decreaseAmount;

  if (creditScore < 0) {
    creditScore = 0;
  }

  document.getElementById("credit-score").textContent = creditScore;
}

setInterval(decreaseCreditScore, 10000);
