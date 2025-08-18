// ==================== TIMER MODULE ====================
const Timer = (function () {
    let seconds = 0;
    let intervalId = null;
    let callbackFn = null;
    let running = false;
    let initialized = false;
    let intervalMs = 1000;

    function formatTime(sec) {
        const m = String(Math.floor(sec / 60)).padStart(2, '0');
        const s = String(sec % 60).padStart(2, '0');
        return `${m}:${s}`;
    }

    function tick() {
        seconds++;
        if (callbackFn) callbackFn(formatTime(seconds));
    }

    return {
        init(cb, opts = {}) {
            if (typeof cb !== 'function') {
                console.error("Timer.init() - callback must be a function");
                return;
            }
            intervalMs = typeof opts.intervalMs === 'number' && opts.intervalMs > 0 ? opts.intervalMs : 1000;
            callbackFn = cb;
            initialized = true;
            seconds = 0;
            running = false;
            console.log("Timer initialized");
        },
        start() {
            if (!initialized) {
                console.warn("Timer.start() - Timer not initialized. Call init(cb) first.");
                return;
            }
            if (running) {
                console.warn("Timer.start() - Timer already running.");
                return;
            }
            running = true;
            intervalId = setInterval(tick, intervalMs);
            console.log("Timer started");
        },
        pause() {
            if (!running) {
                console.warn("Timer.pause() - Timer is not running.");
                return;
            }
            clearInterval(intervalId);
            running = false;
            console.log("Timer paused");
        },
        stop() {
            if (!initialized) {
                console.warn("Timer.stop() - Timer not initialized.");
                return;
            }
            clearInterval(intervalId);
            seconds = 0;
            running = false;
            initialized = false; 
            console.log("Timer stopped - reinit required before start");
        },
        getSec() {
            return seconds;
        }
    };
})();
