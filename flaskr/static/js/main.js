$( document ).ready(function() {

      var clock = $('.clock').FlipClock({
          clockFace: 'TwentyFourHourClock'
      });

      $('.media-object').error(function(){
        $(this).attr('src', 'static/img/logo.png');
        console.log('error?');
      });

      /* Looping through events */
      var numberOfdataEements = $('.singleEvent').length;
      var timeInterval = 14000 * numberOfdataEements;

      if(numberOfdataEements > 1){
        displayScreenLoop();
      }

      function displayScreenLoop(numberOfdataEements){
        setInterval(function(){
          console.log("time interval is : " + timeInterval);
          slideshowLoop();
        }, timeInterval);

        function slideshowLoop(){
          $('#eventTiles .singleEvent').each(function(index) {
            var $div = $(this);
            setTimeout(function() {
              $div.addClass('grow').delay(10000).queue(function(next){
                $div.addClass('shrink').delay(1000).queue(function(next){
                  $div.removeClass('grow shrink');
                  next();
                });
                next();
              });
            }, 11000 * index);
          });
        }
      }

  });
