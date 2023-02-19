var BlazorAudioRecorder = {};

(function () {
    var mStream;
    var mAudioChunks;
    var mMediaRecorder;
    var mCaller;

    BlazorAudioRecorder.Initialize = function (vCaller) {
        mCaller = vCaller;
    };

    BlazorAudioRecorder.StartRecord = async function () {
        mStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mMediaRecorder = new MediaRecorder(mStream);
        mMediaRecorder.addEventListener('dataavailable', vEvent => {
            mAudioChunks.push(vEvent.data);
        });

        mMediaRecorder.addEventListener('error', vError => {
            console.warn('media recorder error: ' + vError);
        });

        mMediaRecorder.addEventListener('stop', () => {
            var pAudioBlob = new Blob(mAudioChunks, { type: "audio/mp3;" });
            var pAudioUrl = URL.createObjectURL(pAudioBlob);
            mCaller.invokeMethodAsync('OnAudioUrl', pAudioUrl);

            // uncomment the following if you want to play the recorded audio (without the using the audio HTML element)
            //var pAudio = new Audio(pAudioUrl);
            //pAudio.play();
        });

        mAudioChunks = [];
        mMediaRecorder.start();
    };

    BlazorAudioRecorder.StopRecord = function () {
        mMediaRecorder.stop();
        mStream.getTracks().forEach(pTrack => pTrack.stop());
    };

    BlazorAudioRecorder.CancelRecord = function () {
        mMediaRecorder.stop();
    };
})();