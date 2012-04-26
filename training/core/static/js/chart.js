var graph = function (data) {
    var chart = document.getElementById('chart')

    var derive_width = function(value, max) {
        return Math.floor((value/max)*400);
    };

    for (var key in data) {
        if (data.hasOwnProperty(key)) {
            var item = data[key];
            var max = Math.max(item.real, item.goal);
            var label = document.createElement('p');
            var real = document.createElement('div');
            var goal = document.createElement('div');

            label.appendChild(document.createTextNode(key
                                                      + " goal:"
                                                      + item.goal
                                                      +  " real:"
                                                      + item.real));
            chart.appendChild(label);
            real.setAttribute('id', item + 'Bar');
            real.setAttribute('class', 'real');
            real.style.width = derive_width(item.real, max) + 'px';
            label.appendChild(real);
            goal.setAttribute('class', 'goal');
            goal.style.width = derive_width(item.goal, max) + 'px';
            goal.appendChild(document.createTextNode('\u00a0'));
            real.appendChild(goal);
        }
    }
};
