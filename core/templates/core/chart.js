var graph = function (data) {
    var chart = document.getElementById('chart')

    var derive_width = function(value, max) {
        return Math.floor((value/max)*400);
    };

    data.forEach(function(item) {
        var max = Math.max(item.real, item.goal);
        var label = document.createElement('p');
        label.appendChild(document.createTextNode(item.type
                                                  + " goal:"
                                                  + item.goal
                                                  +  " real:"
                                                  + item.real));
        chart.appendChild(label);
        var real = document.createElement('div');
        real.setAttribute('id', item.type + 'Bar');
        real.setAttribute('class', 'real');
        real.style.width = derive_width(item.real, max) + 'px';
        label.appendChild(real);
        var goal = document.createElement('div');
        goal.setAttribute('class', 'goal');
        goal.style.width = derive_width(item.goal, max) + 'px';
        goal.appendChild(document.createTextNode('\u00a0'));
        real.appendChild(goal);
    });
};
