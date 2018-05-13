


console.log("SEPHORA JS")




$("#promo-extraction").click(function(){

  console.log("Extraction promos")

  $.ajax({
    url: "/sephora/promos",
    dataType:"json",
    // data: JSON.stringify({"node_data":node_data,"network_data":data}),
    contentType:"application/json",
    type: 'POST',
    success: function(response) {
        // $('#loading').hide();
        console.log("RESPONSE");
        console.log(response);

        data = response["data"];
        carousel = create_carousel(data);

        console.log(carousel);
        $("#promo-results").html(carousel);

    },
    error: function(error) {
        console.log(error);
    }
  });



});



function create_carousel(data){


  template = "";

  for (i = 0; i < data.length; i++) {

    var promo = data[i];
    var img = promo["img"];
    var texts = promo["text"];

    text_template = "";
    for (j = 0; j < texts.length; j++) {
      text = texts[j]
      text_template += `<p>${text}</p>`;  
    }


    template += `
    <div class="promo-result row">
      <div class="col-md-4 img-promo-container">
        <img src=${img} class="img-promo-result"/>
      </div>

      <div class="col-md-8 text-promo-container">
        ${text_template}
      </div>
    </div>
    `;


  }


  return template;
}


