var BlazorAudioPlayer = {};

(function () {
    var mCaller;
    var soundPlayer;
    var soundPlayerNoise;

    BlazorAudioPlayer.Initialize = function (vCaller) {
        mCaller = vCaller;
        soundPlayer = document.getElementById('sound');
        soundPlayerNoise = document.getElementById('sound_noise');

        soundPlayer.addEventListener('ended', () => {
            mCaller.invokeMethodAsync('OnPlayAudioFinished');
        });

        soundPlayerNoise.addEventListener('ended', () => {
            mCaller.invokeMethodAsync('OnPlayAudioFinished');
        });
    };

    window.PlaySound = function (noise) {
        if (noise) {
            soundPlayerNoise.play();
        }
        else {
            soundPlayer.play();
        }
    }

    window.StopSound = function (noise) {
        if (noise) {
            soundPlayerNoise.pause();
            soundPlayerNoise.currentTime = 0;
        }
        else {
            soundPlayer.pause();
            soundPlayer.currentTime = 0;
        }
    }

})();


