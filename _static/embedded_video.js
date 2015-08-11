/***** Embedded video *****/
var array_video_embed = new Array();
var tag = document.createElement('script');
tag.src = "https://www.youtube.com/player_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

function onYouTubePlayerAPIReady() {
    for(key in array_video_embed) {
        var player = new YT.Player(key, array_video_embed[key]);
    }
}

function onPlayerStateChange(event) {
    var data = {};
    // var video_id = event.target.b.b.videoId;
    var url = event.target.getVideoUrl();
    // "http://www.youtube.com/watch?v=gzDS-Kfd5XQ&feature=..."
    var match = url.match(/[?&]v=([^&]+)/);
    // ["?v=gzDS-Kfd5XQ", "gzDS-Kfd5XQ"]
    var video_id = match[1];
    var video_time = event.target.getCurrentTime();
    data['TIME'] = video_time;
    switch (event.data){
    case YT.PlayerState.PLAYING:
	data['PLAY'] = video_id;
        break;
    case YT.PlayerState.ENDED:
	data['END'] = video_id;
        break;
    case YT.PlayerState.PAUSED:
	data['PAUSED'] = video_id;
        break;
    case -1:
	data['LOADED'] = video_id;
	break;
    default:
	return;
    }
    dynsite_send_data(given_uid, "embedded-video", data);
}
