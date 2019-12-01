$(document).ready(function(){
    var larg = (window.innerWidth);
    alert (larg)

    if (larg < 1000) {
        $("#rubrique").hide();
        $("#select").hide();
    }

   $("#card").hide();
   $("#card2").hide();
   $("#card3").hide();
   $("#card4").hide();
   $("#vidéo").hide();
   $("#musicothérapie").hide();
   $("#yoga_description").hide();
   $("#yoga_description").fadeIn(2000);

  $(".ateliers").animate({
    height: '+=30px',
  });


  $("#play").click(function(){
    $("#card").fadeIn();
    $("#card2").fadeIn();
    $("#card3").fadeIn();
    $("#card4").fadeIn();
  });


  $("#card").mouseenter(function(){
    $(this).addClass("border-success");
  });
  $("#card2").mouseenter(function(){
    $(this).addClass("border-success");
  });
  $("#card3").mouseenter(function(){
    $(this).addClass("border-success");
  });
  $("#card4").mouseenter(function(){
    $(this).addClass("border-success");
  });

  $("#card").mouseleave(function(){
    $(this).removeClass("border-success").fadeIn();
  });
  $("#card2").mouseleave(function(){
    $(this).removeClass("border-success").fadeIn();
  });
  $("#card3").mouseleave(function(){
    $(this).removeClass("border-success").fadeIn();
  });
  $("#card4").mouseleave(function(){
    $(this).removeClass("border-success").fadeIn();
  });

  $("#pourquoi").click(function(){
    $("#text_pourquoi").toggle(1000);
  });

  $("#comment").click(function(){
    $("#text_comment").toggle(1000);
  });

  $("#show_video").click(function(){
    $("#vidéo").fadeToggle(1000);
    $("#musicothérapie").hide();
  });

  $("#show_music").click(function(){
    $("#vidéo").hide();
    $("#musicothérapie").fadeToggle(1000);
  });

$("#nav_bar").mouseenter(function(){
  $(".mr-5").animate({
    width: '+=10px',
  });
});

$("#nav_bar").mouseleave(function(){
  $(".mr-5").animate({
    width: '-=10px',
  });
});

//Animation de la page Yoga
  $(".js-scrollTo").click(function() {
	var page = $(this).attr('href');
	console.log(page)
    $("body,html").animate(
      {
        scrollTop: $(page).offset().top
      },
      2000 //speed
    );
  });

//Animation général pour remonter en haut du site.
  $("#scroll-up").click(function() {

	console.log("scroll up !")
    $("body,html").animate(
      {
        scrollTop: $("#nav_bar").offset().top
      },
      1500 //speed
    );
  });

  $("#show_music").mouseenter(function(){
    $(this).removeClass("bg-vert").fadeIn(1000);
    $(this).addClass("bg-vert2").fadeIn(1000);
  });

  $("#show_music").mouseleave(function(){
    $(this).removeClass("bg-vert2").fadeIn(1000);
    $(this).addClass("bg-vert").fadeIn(1000);
  });

  $("#show_video").mouseenter(function(){
    $(this).removeClass("bg-vert").fadeIn(1000);
    $(this).addClass("bg-vert2").fadeIn(1000);
  });

  $("#show_video").mouseleave(function(){
    $(this).removeClass("bg-vert2").fadeIn(1000);
    $(this).addClass("bg-vert").fadeIn(1000);
  });

var DeleteAjax = $(".DeleteAjax");
var idAtelier = $(".DeleteAjax");
DeleteAjax.click(function(event){

    event.preventDefault();
        thisForm = $(this)
        var actionEndpoint = thisForm.attr("action");
        var httpMethod = thisForm.attr("method");
        var formData = thisForm.serialize();
        function extraitNombre(str){ return Number(str.replace(/[^\d]/g, "")) };
        let idAtelier = extraitNombre(actionEndpoint);
        let divAtelier = "#atelier"+idAtelier
        var hideAtelier = $(divAtelier);
            $.ajax({
                url: actionEndpoint,
                method: httpMethod,
                data: formData,

                    success:function(data){
                        console.log("success")
                        hideAtelier.fadeOut(1000)
                    },
                    error:function(errorData){
                        console.log("error")
                        console.log(errorData)
                    }
                })
        })
});