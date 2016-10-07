$(window).ready(function(){
    function playVideo(on=true)
    {
        var play = $('i.video-play');
        if(on)
            play.hide();
        else
            play.show();

        var player = play.prev();
        if(player && player.hasClass('vk_video')) {
            if(on)
                player.show();
            else
                player.hide();
            player.find('.videoplayer_controls_item.videoplayer_btn.videoplayer_btn_play').click();
        }
    }

    $('i.video-play').click(playVideo);
    $('a.flex-next').click(function(){playVideo(false);});
    $('a.flex-prev').click(function(){playVideo(false);});
});
