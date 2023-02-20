var BlazorAudioRecorder = {};

(function () {
    var mStream;
    var mAudioChunks;
    var mMediaRecorder;
    var mCaller;
    var canceled = false;

    BlazorAudioRecorder.Initialize = function (vCaller) {
        mCaller = vCaller;
    };


    BlazorAudioRecorder.StartRecordNew = async function () {
        mStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const options = {
            audioBitsPerSecond: 128000
        };

        mMediaRecorder = new MediaRecorder(stream, options);
        

        mMediaRecorder.ondataavailable = (e) => {
            console.log('media available');
            chunks.push(e.data);
        };

        mMediaRecorder.addEventListener('error', vError => {
            console.warn('media recorder error: ' + vError);
        });

        mMediaRecorder.addEventListener('stop', () => {
            console.log('media recorder stop');
            const blob = new Blob(mAudioChunks, { type: "audio/ogg; codecs=opus" });
            var pAudioUrl = URL.createObjectURL(blob);
            mCaller.invokeMethodAsync('OnAudioUrl', pAudioUrl);
        });

        mAudioChunks = [];
        mMediaRecorder.start();
    };


    BlazorAudioRecorder.StartRecord = async function () {
        mStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const options = {
            audioBitsPerSecond: 44100,  // 16kbps
            mimeType: 'audio/webm;codecs=opus'
        }

        if (!MediaRecorder.isTypeSupported('audio/webm;codecs=opus')) {
            console.error('webm is not Supported');
            return;
        }
        else {
            console.log('webm is Supported');
        }

        mMediaRecorder = new MediaRecorder(mStream, options);

        mMediaRecorder.addEventListener('dataavailable', vEvent => {
            console.log('data available');
            mAudioChunks.push(vEvent.data);
        });

        mMediaRecorder.addEventListener('error', vError => {
            console.warn('media recorder error: ' + vError);
        });

        mMediaRecorder.addEventListener('stop', () => {
            if (canceled) {
                canceled = false;
                return;
            }
            console.log('media recorder stop');
            // add wav header to the audio blob
            const blob = new Blob(mAudioChunks, { type: 'audio/webm;codecs=opus' });
            var pAudioUrl = URL.createObjectURL(blob);
            mCaller.invokeMethodAsync('OnAudioUrl', pAudioUrl);
        });

        mAudioChunks = [];
        mMediaRecorder.start();
    };

    BlazorAudioRecorder.StopRecord = function () {
        canceled = false;
        console.log('stop recording');

        mMediaRecorder.stop();
        mStream.getTracks().forEach(pTrack => pTrack.stop());
    };

    BlazorAudioRecorder.CancelRecord = function () {
        canceled = true;
        console.log('cancel recording');


        mMediaRecorder.stop();
        mStream.getTracks().forEach(pTrack => pTrack.stop());
    };

    BlazorAudioRecorder.CreateObjectURL = function (vArray) {
        var pAudioBlob = new Blob([vArray], { type: "audio/wav" });
        var pAudioUrl = URL.createObjectURL(pAudioBlob);
        return pAudioUrl;
    }

})();