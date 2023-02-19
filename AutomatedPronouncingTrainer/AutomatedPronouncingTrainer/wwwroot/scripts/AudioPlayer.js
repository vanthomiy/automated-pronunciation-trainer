var BlazorAudioPlayer = {};

(function () {
    var mCaller;
    var soundPlayer;

    BlazorAudioPlayer.Initialize = function (vCaller) {
        mCaller = vCaller;
        soundPlayer = document.getElementById('sound');

        soundPlayer.addEventListener('stop', () => {
            mCaller.invokeMethodAsync('OnPlayAudioFinished');
        });
    };

    window.PlaySound = function () {
        soundPlayer.play();
    }

    window.StopSound = function () {
        soundPlayer.pause();
        soundPlayer.currentTime = 0;
    }

})();


