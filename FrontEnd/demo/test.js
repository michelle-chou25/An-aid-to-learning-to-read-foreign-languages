function doTTS() {
    var ttsDiv = document.getElementById('bdtts_div_id');
    var ttsAudio = document.getElementById('tts_autio_id');
    var ttsText = document.getElementById('ttsText').value;

    // 文字转语音 lan=zh（语言zh:中文；en:英文；fr:法文；）
    // ie=UTF-8（字符集）per=3（每3个字符停顿）
    //text=“”（需要转换的文字）spd=5（语音播放速度，数字越大越快0-15）
    ttsDiv.removeChild(ttsAudio);
    var au1 = '<audio id="tts_autio_id" autoplay="autoplay">';
    var sss = '<source id="tts_source_id" src="http://tts.baidu.com/text2audio?lan=en&ie=UTF-8&per=3&spd=5&text=' + ttsText + '" type="audio/mpeg">';
    var eee = '<embed id="tts_embed_id" height="0" width="0" src="">';
    var au2 = '</audio>';
    ttsDiv.innerHTML = au1 + sss + eee + au2;

    ttsAudio = document.getElementById('tts_autio_id');

    ttsAudio.play();
  }