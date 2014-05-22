$(document).ready(function() {
    var dropZone = $('#dropZone')

    if (typeof(window.FileReader) == 'undefined') {
        dropZone.text('Upload via input...');
        dropZone.addClass('error');
    }

    dropZone[0].ondragover = function() {
        dropZone.addClass('hover');
        return false;
    };

    dropZone[0].ondragleave = function() {
        dropZone.removeClass('hover');
        return false;
    };

    dropZone[0].ondrop = function(event) {
        event.preventDefault();
        dropZone.removeClass('hover');
        dropZone.addClass('drop');
        
        var file = event.dataTransfer.files[0];
        
        var xhr = new XMLHttpRequest();
        xhr.upload.addEventListener('progress', uploadProgress, false);
        xhr.onreadystatechange = stateChange;
        xhr.open('POST', '/upload');
        xhr.setRequestHeader('X-FILE-NAME', file.name);
        xhr.send(file);
    };

    function uploadProgress(event) {
        var percent = parseInt(event.loaded / event.total * 100);
        dropZone.text('Uploading: ' + percent + '%');
    }

    function stateChange(event) {
        if (event.target.readyState == 4) {
            if (event.target.status == 200) {
                dropZone.text('Done!');
            } else {
                dropZone.text('Wtf!');
                dropZone.addClass('error');
            }
        }
    }
    
});