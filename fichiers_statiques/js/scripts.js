$("#loader").hide()
// Fonction pour remplacer et afficher l'image sélectionnée
$("#import_img").change(function () { 
    const file = this.files[0]; 
    if (file) { 
        let reader = new FileReader(); 
        reader.onload = function (event) {
            $("#rendu_img").attr("src", event.target.result);
            $("#rendu_img").css({"width": "100%", "max-height": "100%"});
        }; 
        reader.readAsDataURL(file); 
    } 
});

// Methode de d'envoie de l'image vers de serveur
$("form").submit(function (e) {
    e.preventDefault();
    $("#loader").show()
    var token =  $("[name=csrfmiddlewaretoken]").val();
    var data = new FormData($('form').get(0));

    $.ajax({
        url: "",
        method : "POST",
        contentType: false,
        processData: false,
        headers:{
        "X-CSRFToken": token
        },
        enctype: 'multipart/form-data',
        dataType : "json",
        data : data,
        success: function (reponse) {
        if (reponse.operation_status == 'ok') {
            $("#rendu_img").attr("src", `data:image;base64,${reponse.donnees_image}`);
            $("#rendu_img").css({"width": "100%", "max-height": "100%"});
            alert(reponse.message)
        } else {
            alert(reponse.message)
        }
        $("#loader").hide()
        },
        error: function (reponse) {
        $("#loader").hide()
        }
    });
});