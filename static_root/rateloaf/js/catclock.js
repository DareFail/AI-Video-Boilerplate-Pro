

  class Cat {
constructor() {
this._eyelids = document.querySelectorAll('.cat__eyes__eyelid');
}
get eyelids() {
return this._eyelids;
}
blink() {
this._eyelids.forEach((eyelid) => eyelid.classList.add('blink'));
}
}
class Needles {
constructor() {
this.needle = {
sec: document.getElementById('sec'),
min: document.getElementById('min'),
hour: document.getElementById('hour')
};
}
rotate(deg) {
this.needle.sec.style.transform = `rotateZ(${deg.sec}deg)`;
this.needle.min.style.transform = `rotateZ(${deg.min}deg)`;
this.needle.hour.style.transform = `rotateZ(${deg.hour}deg)`;
}
}
const increment = {
sec: (360 / 60),
min: (360 / 60),
hour: (360 / 12)
};
class Clock {
constructor() {
this.needles = new Needles;
this.cat = new Cat;
this.run();
}

run() {
const date = new Date();
const sec = date.getSeconds();
const min = date.getMinutes();
const hour = date.getHours();
const deg = {
sec: sec * increment.sec,
min: min * increment.min,
hour: hour * increment.hour + min * (360 / 12 / 60)
};
this.cat.blink();
this.needles.rotate(deg);
requestAnimationFrame(this.run.bind(this));
}
}
const clock = new Clock;

