var pauseButton = $('button#pause');
var hideButton = $('button#hide');
var addMinuteButton = $('button#addMinute');
var subtractMinuteButton = $('button#subtractMinute');

var duration = moment.duration(0, 'seconds');
var currentTimer = null;
var hidden = false;
var paused = true;

addMinuteButton.click(function () {
    if (duration) {
        var second = moment.duration(1, 'minute');
        duration.add(second);
    }
});

subtractMinuteButton.click(function () {
    if (duration) {
        var second = moment.duration(1, 'minute');
        duration.subtract(second);
    }
});

pauseButton.click(function () {
    paused = !paused;
    if (paused) {
        pauseButton.find('i').removeClass('fa-pause');
        pauseButton.find('i').addClass('fa-play');
    } else {
        pauseButton.find('i').removeClass('fa-play');
        pauseButton.find('i').addClass('fa-pause');
    }
});

hideButton.click(function () {
    hidden = !hidden;
    if (hidden) {
        hideButton.find('i').removeClass('fa-eye-slash');
        hideButton.find('i').addClass('fa-eye');
    } else {
        hideButton.find('i').removeClass('fa-eye');
        hideButton.find('i').addClass('fa-eye-slash');
    }
});

function startTimer(timerId) {
    currentTimer = $("#" + timerId);
    duration = moment.duration(parseInt(currentTimer.attr('data-seconds')), 'seconds');

    paused = false;
    $('.pulsate').removeClass('pulsate');
    currentTimer.find('button.pause').addClass('pulsate');
}
